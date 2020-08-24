from surfaces.surface import Surface
from ray.ray import Ray
from ray.rays_pool import RaysPool
import numpy as np
import math as m


class Sphere(Surface):
    """
        (r-p0,r-p0) = R^2 - canonical equation of sphere
        :argument center - сооrdinate of sphere center
        :argument radius - radius of sphere
        :argument type_surface - reflecting or refracting surface
        :argument n1,n2 - refractive indexes of space. watch method get_refractive_indexes in class Surface
    """

    def __init__(self, center: list, radius: float,
                 type_surface: Surface.types = Surface.types.REFLECTING,
                 n1: float = 1,
                 n2: float = 1):
        if n1 < 1 or n2 < 1:
            raise AttributeError("Refractive indices less than unity. n1: {}, n2: {}".format(n1, n2))
        if not all(isinstance(i, float) or isinstance(i, int) for i in center):
            raise AttributeError("""Some element in %s is not a float number.""" % (str(center)))

        Surface.__init__(self, type_of_surface=type_surface, dimension=len(center))
        self.__center = center.copy()
        self.__r = radius
        self._Surface__n1 = n1
        self._Surface__n2 = n2

    # =========================== getter and setter ====================================================================

    @property
    def center(self):
        return self.__center

    @property
    def r(self):
        return self.__r

    # ============================== Sphere object methods =============================================================

    def __str__(self):
        return "Sphere:{ center: %s, radius: %s, type: %s}" % (str(self.center), str(self.r), str(self.type))

    # def draw_surface(self, axes, color='b', alpha=0.5) -> bool:
    #     if self.dim == 2:
    #
    #     elif self.dim == 3:
    #         u = np.linspace(0, 2 * np.pi, 100)
    #         v = np.linspace(0, np.pi, 100)
    #
    #         x = np.subtract(self.r * np.outer(np.cos(u), np.sin(v)), -self.center[0])
    #         y = np.subtract(self.r * np.outer(np.sin(u), np.sin(v)), -self.center[1])
    #         z = np.subtract(self.r * np.outer(np.ones(np.size(u)), np.cos(v)), -self.center[2])
    #         print('x = ')
    #         print(x)
    #         print('y = ')
    #         print(y)
    #
    #         axes.plot_surface(x, y, z, rstride=4, cstride=4, color=color, alpha=alpha)
    #         return True
    #
    #     raise AttributeError("Defined only dor dimension 2 and 3")

    def is_point_belong(self, point: (list, tuple)) -> bool:
        if len(point) != self.dim:
            raise AttributeError("The point %s have different dimension than sphere(%s)" % (str(point), str(self.dim)))

        r0 = np.subtract(point, self.center)
        if abs(np.linalg.norm(r0) - self.r) < 10 * np.finfo(float).eps:
            return True

    def norm_vec(self, point):
        # if not self.is_point_belong(point):
        #     raise AttributeError("The point %s is not belong surface %s" % (str(point), str(self)))

        n = []
        for i in range(self.dim):
            n.append(2 * (point[i] - self.center[i]))

        return np.dot(1 / np.linalg.norm(n), n)

    def get_refractive_indexes(self, point: list):
        """
        returns 2 coefficients
        :param point:
        :return: n1,n2
        """
        """
        n1 - outside of sphere
        n2 - on sphere and inside sphere"""
        rad_vec = np.subtract(point, self.center)
        if np.linalg.norm(rad_vec) - self.r > 10 * np.finfo(float).eps:
            return self._Surface__n1, self._Surface__n2
        return self._Surface__n2, self._Surface__n1

    # ======================================= methods for Ray ==========================================================
    def _ray_surface_intersection(self, e: list, r: list) -> list:
        r0_p0 = np.subtract(self.center, r)
        r0_p0e = np.dot(r0_p0, e)
        # ищем дискриминант
        disc = r0_p0e ** 2 - np.dot(r0_p0, r0_p0) + self.r ** 2
        if (abs(disc) < np.finfo(float).eps):
            disc = 0

        if disc < 0:
            return []
        # ищем корни/корень
        t = None
        if (disc != 0):
            sqrt_disc = m.sqrt(disc)
            t = [r0_p0e - sqrt_disc, r0_p0e + sqrt_disc]
        else:
            t = [r0_p0e]

        # проверки
        if all([i < np.finfo(float).eps for i in t]):
            return []
        # массив положительных корней
        positive_t = []
        for i in t:
            if i > 10 * np.finfo(float).eps:
                positive_t.append(i)
        if len(positive_t) > 0:
            return positive_t

    def find_intersection_with_surface(self, ray: Ray) -> list:
        positive_t = Sphere._ray_surface_intersection(self, ray.dir, ray.start)
        if (positive_t is not None) and (len(positive_t) > 0):
            ray.t0 = [positive_t[0], self]
            return [ray.calc_point_of_ray(t) for t in positive_t]
        return []

    # реализация без переноса центра сферы в центр координат(на это нужен только сдвиг)

    def find_nearest_point_intersection(self, ray: Ray):
        l = self.find_intersection_with_surface(ray)
        if l != None and len(l) > 0:
            return l[0]

    # ======================================== methods for Ray_pool ====================================================
    def find_intersection_pool_with_surface(self, pool: RaysPool, index: int):
        return Sphere._ray_surface_intersection(self, pool.e(index), pool.r(index))

    def find_nearest_intersection_pool_with_surface(self, pool, index: int):
        l = self.find_intersection_pool_with_surface(pool, index)
        if l != None and len(l) > 0:
            return l[0]
