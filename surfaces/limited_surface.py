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
        if len(limits) != surface.dim:
            raise AttributeError("Limits(%d) and surface(dim: %d) have different size" % (len(limits), surface.dim))
        if not all(coor[0] < coor[1] for coor in limits):
            raise AttributeError("Invalid limits " + str(limits))
        self.__limits = limits
        self.__surface = surface
        self._Surface__dim = surface.dim

    # =========================== getter and setter ====================================================================

    @property
    def limits(self) -> list:
        return self.__limits

    def set_refractive_indexes(self, n1: float = 1, n2: float = 1):
        self.__surface.set_refractive_indexes(n1, n2)

    # ==========================methods of object=================================================================

    def __str__(self):
        return "Limited " + str(self.__surface) + " limits: " + str(self.__limits)

    # =================================== Plane objects methods ========================================================

    def norm_vec(self, point):
        if self._is_point_in_limits(point):
            return self.__surface.norm_vec(point)
        return None

    def get_refractive_indexes(self, point: list):
        return self.__surface.get_refractive_indexes(point)

    def draw_surface(self, axes) -> bool:
        if isinstance(self.__surface, Plane):
            line = mlines.Line2D(self.limits[0], self.limits[1])
            axes.add_line(line)
            return True
        return False

    def _is_point_in_limits(self, point: list):
        if point is None or not all(
                bounds[0] <= coor and coor <= bounds[1] for coor, bounds in zip(point, self.__limits)):
            return False
        else:
            return True

    def _bounds_filter(self, e: list, r: list, t: float):
        mul = np.multiply(t, e)
        point = list(np.add(mul, r))
        if not self._is_point_in_limits(point):
            return []
        return point

    # ======================================= methods for Ray ==========================================================

    def _ray_surface_intersection(self, e: list, r: list) -> list:
        t = self.__surface._ray_surface_intersection(e, r)
        ans_t = []
        for i in range(len(t)):
            checked_t = self._bounds_filter(e, r, t[i])
            if len(checked_t) != 0:
                ans_t.append(t[i])
        return ans_t

    # """реализация для Плоскоти. Не обощено на все поверности"""
    def find_intersection_with_surface(self, ray):
        positive_t = LimitedSurface._ray_surface_intersection(self, ray.dir, ray.start)
        if len(positive_t) > 0:
            ray.t1 = positive_t[0]
            return [ray.calc_point_of_ray(t) for t in positive_t]
        return []

    def find_nearest_point_intersection(self, ray):
        l = self.find_intersection_with_surface(ray)
        if l != None and len(l) > 0:
            return l[0]
