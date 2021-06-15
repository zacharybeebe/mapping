import shapefile as shp
from parameters import *


class Shape(object):
    def __init__(self, program, map, shapefile, initial_projection=False):
        self.p = program
        self.m = map
        self.shp_name = shapefile
        self.color = DSEAGREEN
        self.feat_pts = self.read_shapefile()
        if initial_projection:
            self.poly_coords = []
            self.point_coords = []
        else:
            self.poly_coords = self.get_poly_coords()
            self.point_coords = self.get_points_coords()



    def read_shapefile(self):
        s = shp.Reader(self.shp_name)
        shapes = s.shapes()
        return [shapes[i].points for i in range(len(shapes))]


    def get_poly_coords(self):
        master = []
        for i, shape in enumerate(self.feat_pts):
            temp = []
            for j, pt in enumerate(shape):
                temp.append((self.m.map_width / 2) - (((self.m.centerx - pt[0]) / (self.m.right - self.m.left)) * self.m.map_width))
                temp.append((self.m.map_height / 2) + (((self.m.centery - pt[1]) / (self.m.top - self.m.bottom)) * self.m.map_height))
                if pt == shape[0] and j != 0 and j != len(shape) - 1:
                    master.append(temp)
                    temp = []
            master.append(temp)
        return master

    def get_points_coords(self):
        master = []
        for shape in self.feat_pts:
            temp = []
            for pt in shape:
                temp.append([(self.m.map_width / 2) - (((self.m.centerx - pt[0]) / (self.m.right - self.m.left)) * self.m.map_width),
                             (self.m.map_height / 2) + (((self.m.centery - pt[1]) / (self.m.top - self.m.bottom)) * self.m.map_height)])
            master.append(temp)
        return master

    # def adjust_poly_coords(self, event):
    #     self.poly_coords = self.get_poly_coords()
    #     for shape in self.poly_coords:
    #         for j, point in enumerate(shape):
    #             if event.delta < 0:
    #                 if j % 2 == 0:
    #                     shape[j] = self.p.mousex + ((point - self.p.mousex) / (1 + self.p.scroll_ratio))
    #                 else:
    #                     shape[j] = self.p.mousey + ((point - self.p.mousey) / (1 + self.p.scroll_ratio))
    #             else:
    #                 if j % 2 == 0:
    #                     shape[j] = self.p.mousex + ((point - self.p.mousex) * (1 + self.p.scroll_ratio))
    #                 else:
    #                     shape[j] = self.p.mousey + ((point - self.p.mousey) * (1 + self.p.scroll_ratio))
    #
    # def align_poly_coords(self, change_x, change_y):
    #     self.poly_coords = self.get_poly_coords()
    #     for shape in self.poly_coords:
    #         for j, point in enumerate(shape):
    #                 if j % 2 == 0:
    #                     shape[j] += change_x
    #
    #                 else:
    #                     shape[j] += change_y




