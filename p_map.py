import tkinter as t
from tkinter import ttk, messagebox, filedialog
import shapefile as shp
import os
from parameters import *
from p_shape import Shape


class Map(object):
    def __init__(self, program):
        self.p = program

        self.left, self.right, self.bottom, self.top = 0, 0, 0, 0
        self.centerx, self.centery = 0, 0

        self.mx, self.my, self.amx, self.amy = 0, 0, 0, 0
        #self.shape_ratio = 0.125
        self.scroll_ratio = 0.075


        self.edit_points, self.edit_lines = [], []
        self.edit_polys = {}
        self.features = []
        self.shapes = []

        self.edit_shapes = {}
        self.current_edit = None
        self.current_poly = 1
        self.edit_mode = False

        self.holdx, self.holdy = 0, 0

        self.no_projection = True

        self.frame_map_canvas_format()
        self.edit_mode_buttons()


    def frame_map_canvas_format(self):
        self.canvas = t.Canvas(self.p.frame_map)
        self.canvas.place(x=0, y=0, relwidth=1.0, relheight=1.0)

        self.p.root.update()
        self.map_width = self.canvas.winfo_width()
        self.map_height = self.canvas.winfo_height()
        self.aspect = self.map_height / self.map_width

        self.canvas.bind('<Enter>', lambda event: self._canvas_bound(event))
        self.canvas.bind('<Leave>', lambda event: self._canvas_unbound(event))



    def edit_mode_buttons(self):
        self.edit_toggle = t.Button(self.p.frame_tool, font=font10Cb, text='Enter Edit Mode', state='disabled')
        self.edit_toggle['command'] = self._toggle_edit_mode
        self.edit_toggle.place(relx=0.025, rely=0.25, relwidth=0.075, relheight=0.5)

        self.edit_create = t.Button(self.p.frame_tool, font=font10Cb, text='Create Polygon', state='disabled')
        self.edit_create['command'] = self._edit_mode_create_get_name
        self.edit_create.place(relx=0.125, rely=0.25, relwidth=0.075, relheight=0.5)

    def _toggle_edit_mode(self):
        self.edit_mode = not self.edit_mode
        if not self.edit_mode:
            self.p.frame_tool['bg'] = ORANGEMED
            self.edit_toggle['text'] = 'Enter Edit Mode'
            self.edit_create['state'] = 'disabled'
        else:
            self.p.frame_tool['bg'] = PALEGREEN
            self.edit_toggle['text'] = 'Exit Edit Mode'
            self.edit_create['state'] = 'normal'

    def _edit_mode_create_get_name(self):
        if self.edit_create['text'] == 'Create Polygon':
            width, height, offx, offy = 400, 200, 400, 100
            top = t.Toplevel()
            top.transient(self.canvas)
            top.geometry(f'{width}x{height}+{offx}+{offy}')
            frame = t.Frame(top, bg=ORANGESOFT, width=width, height=height)
            frame.pack()
            label = t.Label(frame, bg=ORANGESOFT, font=font18Cb, text='SHAPEFILE NAME', anchor='w')
            label.place(relx=0.1, y=0, relwidth=0.8, relheight=0.2)
            entry = t.Entry(frame, font=font10Cb)
            entry.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.15)
            button = t.Button(frame, font=font14Cb, text='Submit')
            button['command'] = lambda tp=top, e=entry: self._edit_mode_create_submit(tp, e)
            button.place(relx=0.1, rely=0.55, relwidth=0.8, relheight=0.3)
        else:
            self._edit_mode_save_poly()
            self._delete_all_canvas_edit_shapes(all_clear=True)
            self.edit_create['text'] = 'Create Polygon'




    def _edit_mode_save_poly(self):
        del self.edit_shapes[self.current_edit][self.current_poly]
        with shp.Writer(self.current_edit) as w:
            w.field('FID', 'N')
            for poly in self.edit_shapes[self.current_edit]:
                p = w.poly([[i[0] for i in self.edit_shapes[self.current_edit][poly]]])
                w.record(p)

        with open(f'{self.current_edit}.prj', 'w') as prj:
            prj.write(NAD_1983_WA_S)

        self.features.append(Shape(self.p, self, self.current_edit))
        self.current_edit = None
        self.project_shapes()


    def _edit_mode_create_submit(self, top, entry):
        name = entry.get()
        filename = os.path.join(self.p.path, name)
        self.current_edit = filename
        self.edit_shapes[self.current_edit] = {}
        self.edit_shapes[self.current_edit][self.current_poly] = []

        self.edit_create['text'] = '*SAVE POLYGON*'
        top.destroy()


    def _canvas_bound(self, event):
        self.canvas.bind('<Motion>', self._mouse_motion)
        if self.edit_mode:
            self.canvas.bind_all('<Button-1>', lambda event:self._edit_canvas_button1_press(event))
            self.canvas.bind_all('<Double-Button-1>', lambda event:self._edit_canvas_double_over(event))
        else:
            self.canvas.bind_all('<MouseWheel>', lambda event: self._canvas_on_mousewheel(event))
            self.canvas.bind_all('<Button-2>', lambda event: self._canvas_on_button2_press(event))
            self.canvas.bind('<B2-Motion>', lambda event: self._canvas_on_button2_hold(event))
            self.canvas.bind_all('<ButtonRelease-2>', lambda event: self._canvas_on_button2_release(event))

    def _canvas_unbound(self, event):
        self.canvas.unbind('<Motion>')
        if self.edit_mode:
            self.canvas.unbind_all('<Button-1>')
            self.canvas.unbind_all('<Double-Button-1>')
        else:
            self.canvas.unbind_all('<MouseWheel>')
            self.canvas.unbind_all('<Button-2>')
            self.canvas.unbind('<B2-Motion>')
            self.canvas.unbind_all('<ButtonRelease-2>')


    def _mouse_motion(self, event):
        self.mx, self.my = event.x, event.y

        if self.edit_mode:
            self._edit_mode_draw_line_or_poly()

        if event.state != 264:
            self.holdx, self.holdy = event.x, event.y

        self._get_mouse_abs()

    def _get_mouse_abs(self):
        self.amx = self.left + ((self.mx / self.map_width) * (self.right - self.left))
        self.amy = self.top - ((self.my / self.map_height) * (self.top - self.bottom))


    def _edit_mode_draw_line_or_poly(self):
        if self.edit_shapes:
            if self.current_edit is not None:
                plist = self.edit_shapes[self.current_edit][self.current_poly]
                length = len(plist)
                if length > 0:
                    if length == 1:
                        self.edit_polys[self.current_poly] = []
                        self._edit_mode_clear_edit_lists(self.edit_lines)
                        self.edit_lines.append(self.canvas.create_line(self.mx, self.my, plist[0][1][0], plist[0][1][1]))
                    else:
                        self._edit_mode_clear_edit_lists(self.edit_lines)
                        self._edit_mode_clear_edit_lists(self.edit_polys[self.current_poly])
                        self.edit_polys[self.current_poly].append(self.canvas.create_polygon(self._edit_mode_get_poly_coords(),
                                                                                             fill=ORANGESOFT, outline=BLACK))

    def _edit_mode_clear_edit_lists(self, edit_list):
        for i in edit_list:
            self.canvas.delete(i)



    def _edit_mode_get_poly_coords(self):
        poly_coords = []
        for i in self.edit_shapes[self.current_edit][self.current_poly]:
            poly_coords.append(i[1][0])
            poly_coords.append(i[1][1])
        poly_coords.append(self.mx)
        poly_coords.append(self.my)
        poly_coords.append(poly_coords[0])
        poly_coords.append(poly_coords[1])
        return poly_coords







    def _edit_canvas_button1_press(self, event):
        if self.current_edit is not None:
            coords = [[self.amx, self.amy], [self.mx, self.my]]
            self.edit_shapes[self.current_edit][self.current_poly].append(coords)
            radius = 2.5
            self.edit_points.append(self.canvas.create_oval(self.mx-radius, self.my-radius, self.mx+radius, self.my+radius,
                                                            fill=DARKRED))


    def _edit_canvas_double_over(self, event):
        self._delete_all_canvas_edit_shapes()
        self.current_poly += 1
        self.edit_shapes[self.current_edit][self.current_poly] = []


    def _delete_all_canvas_edit_shapes(self, all_clear=False):
        deletes = [self.edit_points, self.edit_lines]
        for i in deletes:
            self._edit_mode_clear_edit_lists(i)
        if all_clear:
            for poly in self.edit_polys:
                self._edit_mode_clear_edit_lists(self.edit_polys[poly])



    def _canvas_on_button2_press(self, event):
        self.holdx, self.holdy = event.x, event.y
        self.p.root['cursor'] = 'fleur'

    def _canvas_on_button2_hold(self, event):
        self._change_alignment_button2_hold(event)

        if len(self.features) > 0:
            for feat in self.features:
                feat.poly_coords = feat.get_poly_coords()
            self.project_shapes()

    def _canvas_on_button2_release(self, event):
        self.p.root['cursor'] = 'arrow'

    def _canvas_on_mousewheel(self, event):
        if not self.no_projection:
            self._change_scale(event)
            self._change_alignment_mousewheel()

            if len(self.features) > 0:
                for feat in self.features:
                    feat.poly_coords = feat.get_poly_coords()
                self.project_shapes()



    def _change_scale(self, event):
        if event.delta < 0 :
            difx = (self.right - self.left) * (1 + self.scroll_ratio)
            dify = difx * self.aspect
        else:
            difx = (self.right - self.left) / (1 + self.scroll_ratio)
            dify = difx * self.aspect

        change_x = (difx - ((self.right - self.left))) / 2
        change_y = (dify - ((self.top - self.bottom))) / 2

        self.right += change_x
        self.left -= change_x
        self.top += change_y
        self.bottom -= change_y

        self._get_centers()
        self._get_mouse_abs()


    def _change_alignment_mousewheel(self):
        adjust = 2000
        shiftx = self.left * ((self.mx - (self.map_width / 2)) / self.map_width) / adjust
        shifty = self.top * ((self.my - (self.map_height / 2)) / self.map_height) / adjust

        self.left += shiftx
        self.right += shiftx
        self.bottom -= shifty
        self.top -=shifty

        self._get_centers()
        self._get_mouse_abs()

    def _change_alignment_button2_hold(self, event):
        change_x = event.x - self.holdx
        change_y = event.y - self.holdy

        adjust = 25

        shiftx = (self.right - self.left) * (change_x / self.map_width) / adjust
        shifty = (self.top - self.bottom) * (change_y / self.map_height) / adjust

        self.left -= shiftx
        self.right -= shiftx
        self.bottom += shifty
        self.top += shifty

        self._get_centers()
        self._get_mouse_abs()

        if abs(change_x) > adjust * 7.5:
            self.holdx = event.x
        if abs(change_y) > adjust * 7.5:
            self.holdy = event.y


    def _get_centers(self):
        self.centerx = (self.right + self.left) / 2
        self.centery = (self.top + self.bottom) / 2


    def get_inital_coords(self, shape_list):
        minx, maxx, miny, maxy, adjust_x, adjust_y = self._get_initial_coords_get_adjust(shape_list)

        self.left = minx - adjust_x
        self.right = maxx + adjust_x
        self.bottom = miny - adjust_y
        self.top = maxy + adjust_y

        self._get_centers()
        self._get_mouse_abs()
        self.no_projection = False
        self.edit_toggle['state'] = 'normal'
        self.p.root.title('ZAPPER')

        for shapes in shape_list:
            shapes.poly_coords = shapes.get_poly_coords()
            self.features.append(shapes)


    def _get_initial_coords_get_adjust(self, shape_list):
        x_list = []
        y_list = []
        for shapes in shape_list:
            for shape in shapes.feat_pts:
                for points in shape:
                    x_list.append(points[0])
                    y_list.append(points[1])

        minx, maxx = min(x_list), max(x_list)
        miny, maxy = min(y_list), max(y_list)

        scalex = (maxx - minx) * (1 + (self.scroll_ratio * 10))
        scaley = scalex * self.aspect

        adjust_x = (scalex - (maxx - minx)) / 2
        adjust_y = (scaley - (maxy - miny)) / 2

        return minx, maxx, miny, maxy, adjust_x, adjust_y



    def project_shapes(self):
        for i in self.shapes:
            self.canvas.delete(i)

        for feat in self.features:
            for pts in feat.poly_coords:
                self.shapes.append(self.canvas.create_polygon(pts, fill=feat.color, outline=BLACK))


