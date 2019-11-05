from surfaces.plane import Plane
from surfaces.surface import Surface
import matplotlib.lines as mlines
import numpy as np


class LimitedSurface(Surface):
    @staticmethod
    def checks():
        pass

    """
        limits must to have array of two-dimension array with left and right bounds. Length of limits must to equal with dimension of surface
    """

    def __init__(self, surface: Surface, limits: list):
        self.__limits = limits
        self.__surface = surface
        self._Surface__dim = surface.dim

    def norm_vec(self, point):
        return self.__surface.norm_vec(point)

    def get_refractive_indexes(self, point: list):
        return self.__surface.get_refractive_indexes(point)

    def draw_surface(self, axes) -> bool:
        m = [[0, -1],
             [1, 0]]
        # direction vector
        r = np.dot(m, self.norm_vec([0, 0]))
        point1 = np.dot(self.__limits[0][0], r)
        point2 = np.dot(self.__limits[0][1], r)
        points = [point1, point2]

        print("points")
        print(points)

        def calc_point(start: list, dir, leng):
            poin = []
            for i in range(len(start)):
                poin.append(start[i] + dir[i] * leng)
            return poin

        line = mlines.Line2D([val[0] for val in points], [val[1] for val in points])
        axes.add_line(line)
        return True

    # """реализация для Плоскоти. Не обощено на все поверности"""
    def find_intersection_with_surface(self, ray):
        print("aaa")
        point = self.__surface.find_nearest_point_intersection(ray)

        if point is None or not all(
                bounds[0] <= coor and coor <= bounds[1] for coor, bounds in zip(point, self.__limits)):
            return None
        return point

    def find_nearest_point_intersection(self, ray):
        return self.find_intersection_with_surface(ray)

    def __str__(self):
        return "Limited " + str(self.__surface) + " limits: " + str(self.__limits)
