from ray.ray import Ray
from surfaces.surface import Surface
import matplotlib.patches as pathes
import numpy as np
import math as m


class Ellipse(Surface):
    __center = []
    __abc = []
    """
    (x-x0)^2/a^2 + (y - y0)^2/b^2 + (z - z0)^2/c^2 = 1 - canonical equation of ellipse
    :argument center - сооrdinate of ellipse center  
    :argument ellipse_coefficients - a,b,c in canonical equation of ellipse
    :argument type_surface - reflecting or refracting surface
    :argument n1,n2 - refractive indexes of space. watch method get_refractive_indexes in class Surface
    """

    def __init__(self, center: (list,iter), ellipse_coefficients: (list,iter),
                 type_surface: Surface.types = Surface.types.REFLECTING,
                 n1: float = 1,
                 n2: float = 1):
        if len(center) != len(ellipse_coefficients):
            raise AttributeError("""Iterables objects have different length. 
            len(center): %d,
            len(ellipse_coefficients): %d""" % (len(center), len(ellipse_coefficients)))

        if n1 < 1 or n2 < 1:
            raise AttributeError("Refractive indices less than unity. n1: {}, n2: {}".format(n1, n2))
        if not all(isinstance(i, int) or
                   isinstance(j, int) or
                   isinstance(i, float) or
                   isinstance(j, float) for i, j in
                   zip(center, ellipse_coefficients)):
            raise AttributeError(
                """Some element in %s or %s is not a digit.""" % (str(center), str(ellipse_coefficients)))
        self._Surface__dim = len(center)
        self._Surface__type_of_surface = type_surface
        self.__center = list(center).copy()
        self.__abc = list(ellipse_coefficients).copy()
        self._Surface__n1 = n1
        self._Surface__n2 = n2

    # =========================== getter and setter ====================================================================

    @property
    def center(self):
        return self.__center

    @property
    def abc(self):
        return self.__abc

    # ============================== Ellipse object methods ============================================================

    def __str__(self):
        return "Ellipse{ center: %s, coef: %s, type: %s}" % (str(self.center), str(self.abc), str(self.type))

    def draw_surface(self, axes, color='b', alpha=0.5) -> bool:
        if self.dim == 2:
            ellipse = pathes.Ellipse(self.center, 2 * self.abc[0], 2 * self.abc[1], fill=False)
            axes.add_patch(ellipse)
            del ellipse
            return True
        elif self.dim == 3:
            u = np.linspace(0, 2 * np.pi, 100)
            v = np.linspace(0, np.pi, 100)

            x = np.subtract(self.abc[0] * np.outer(np.cos(u), np.sin(v)), -self.center[0])
            y = np.subtract(self.abc[1] * np.outer(np.sin(u), np.sin(v)), -self.center[1])
            z = np.subtract(self.abc[2] * np.outer(np.ones(np.size(u)), np.cos(v)), -self.center[2])

            axes.plot_surface(x, y, z, rstride=4, cstride=4, color=color, alpha=alpha)
            return True

        raise AttributeError("Defined only dor dimension 2 and 3")

    def is_point_belong(self, point: (list, tuple)) -> bool:
        if len(point) != self.dim:
            raise AttributeError("The point %s have different dimension than ellipse(%s)" % (str(point), str(self.dim)))

        sum = 0
        for i in range(self.dim):
            sum += ((point[i] - self.center[i]) ** 2) / (self.abc[i] ** 2)

        if abs(sum - 1) < 10 * np.finfo(float).eps:
            return True

    def norm_vec(self, point: list):
        # if not self.is_point_belong(point):
        #     raise AttributeError("The point %s is not belong surface %s" % (str(point), str(self)))
        n = []
        for i in range(self.dim):
            n.append((2 * (point[i] - self.center[i])) / (self.abc[i] ** 2))

        return np.dot(1 / np.linalg.norm(n), n)

    def get_refractive_indexes(self, point: list):
        """
        :param point:
        :return n1,n2:
        """
        """
        n1 - outside of ellipse
        n2 - on ellipse and inside ellipse"""
        sum = 0
        for i in range(self.dim):
            sum += ((point[i] - self.center[i]) ** 2) / (self.abc[i] ** 2)

        if sum - 1 > 10 * np.finfo(float).eps:
            return self._Surface__n1, self._Surface__n2
        return self._Surface__n2, self._Surface__n1

    # ======================================= methods for Ray ==========================================================
    def _ray_surface_intersection(self, e: list, r: list) -> list:
        r_p0 = np.subtract(r, self.center)
        mat = []
        abc = 0
        if len(r) == 3:
            mat = [[self.abc[1] * self.abc[2], 0, 0],
                   [0, self.abc[0] * self.abc[2], 0],
                   [0, 0, self.abc[0] * self.abc[1]]]

            abc = mat[0][0] * mat[1][1] * mat[2][2]
        elif len(r) == 2:
            mat = [[self.abc[1], 0],
                   [0, self.abc[0]]]
            abc = self.abc[1] ** 2 * self.abc[0] ** 2
        mr_p0 = np.dot(mat, r_p0)
        me = np.dot(mat, e)

        a = np.dot(me, me)
        b = np.dot(me, mr_p0)
        c = np.dot(mr_p0, mr_p0) - abc
        # ищем дискриминант
        disc_on4 = b ** 2 - a * c
        if abs(disc_on4) < np.finfo(float).eps:
            disc_on4 = 0
        if disc_on4 < 0:
            return []
        sqrt_disc_on4 = m.sqrt(disc_on4)
        # ищем корни/корень
        if disc_on4 == 0:
            t = [-b / a]
        else:
            t = [(-b - sqrt_disc_on4) / a, (-b + sqrt_disc_on4) / a]
        # пр    оверки
        if all([i < 0 for i in t]):
            return []
        # массив положительных корней
        positive_t = []
        for i in t:
            if i > 10 * np.finfo(float).eps:
                positive_t.append(i)
        if len(positive_t) > 0:
            return positive_t

    def find_intersection_with_surface(self, ray: Ray) -> list:
        positive_t = Ellipse._ray_surface_intersection(self, ray.dir, ray.start)
        if len(positive_t) > 0:
            ray.t0 = [positive_t[0], self]
            return [ray.calc_point_of_ray(t) for t in positive_t]
        return []

    def find_nearest_point_intersection(self, ray: Ray):
        l = self.find_intersection_with_surface(ray)
        if l is not None and len(l) > 0:
            return l[0]

    # ======================================== methods for Ray_pool ====================================================
    def find_intersection_pool_with_surface(self, pool, index: int):
        return Ellipse._ray_surface_intersection(self, pool.e(index), pool.r(index))

    def find_nearest_intersection_pool_with_surface(self, pool, index: int):
        l = self.find_intersection_pool_with_surface(pool, index)
        if l != None and len(l) > 0:
            return l[0]
