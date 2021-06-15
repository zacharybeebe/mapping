import tkinter as t
from tkinter import ttk, messagebox, filedialog
import shapefile as shp
import os
import math
import time
from parameters import *
from p_map import Map
from p_shape import Shape



class Program(object):
    def __init__(self):
        self.path = os.getcwd()
        self.root = t.Tk()
        self.root.geometry(f'{self.root.winfo_screenwidth() - 24}x{self.root.winfo_screenheight() - 80}+5+5')
        self.root.title('ZAPPER  *unprojected*')

        self.frame_tool_format(INITIAL_FRAME_LAYOUT['FT'])
        self.frame_side_format(INITIAL_FRAME_LAYOUT['FS'])
        self.frame_map_format(INITIAL_FRAME_LAYOUT['FM'])

        self.map = Map(self)



    def frame_tool_format(self, layout):
        self.frame_tool = t.Frame(self.root, bg=ORANGEMED)
        self.frame_tool.place(x=layout[0], y=layout[1], relwidth=layout[2], relheight=layout[3])


    def frame_side_format(self, layout):
        self.frame_side = t.Frame(self.root, bg=ORANGESOFT)
        self.frame_side.place(x=layout[0], rely=layout[1], relwidth=layout[2], relheight=layout[3])

        up_shp_button = t.Button(self.frame_side, font=font10Cb, text='Upload Shapefile', height=30)
        up_shp_button['command'] = self._upload_shapefile
        up_shp_button.place(x=0, y=0, relwidth=1.0, relheight=0.05)


    def _upload_shapefile(self):
        shape_names = filedialog.askopenfilenames(initialdir=self.path, title='Upload Shapefile',
                                                  filetypes=(('Shapefile', '*.shp'), ('All Files', '*.*')))

        if len(shape_names) > 0:
            if self.map.no_projection:
                shape_list = [Shape(self, self.map, shape_name, initial_projection=self.map.no_projection) for shape_name in shape_names]
                self.map.get_inital_coords(shape_list)
            else:
                for shape_name in shape_names:
                    new_shape = Shape(self, self.map, shape_name, initial_projection=self.map.no_projection)
                    self.map.features.append(new_shape)
            self.map.project_shapes()




    def frame_map_format(self, layout):
        self.frame_map = t.Frame(self.root, bg=PALEGREEN)
        self.frame_map.place(relx=layout[0], rely=layout[1], relwidth=layout[2], relheight=layout[3])








