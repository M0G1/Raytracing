from surfaces.surface import Surface
import matplotlib.patches as pathes
from ray.ray import Ray
import numpy as np
import math as m


class Sphere(Surface):
    __center = []
    __r = 0.

    def __init__(self, center: list, radius: float,
                 type_surface: Surface.types = Surface.types.REFLECTING,
                 n1: float = 1,
                 n2: float = 1):
        if n1 < 1 or n2 < 1:
            raise AttributeError("Refractive indices less than unity. n1: {}, n2: {}".format(n1, n2))
        if not all(isinstance(i, float) or isinstance(i, int) for i in center):
            raise AttributeError("""Some element in %s is not a float number.""" % (str(center)))

        self._Surface__dim = len(center)
        self._Surface__type_of_surface = type_surface
        self.__center = center.copy()
        self.__r = radius
        self.__n1 = n1
        self.__n2 = n2

    # getter and setter====================================================================

    @property
    def center(self):
        return self.__center

    @property
    def r(self):

        return self.__r

    # methods of object sphere====================================================================

    def __str__(self):
        return "Sphere:{ center: %s, radius: %s, type: %s}" % (str(self.center), str(self.r), str(self.type))

    def draw_surface(self, axes, color='b', alpha=0.5) -> bool:
        if self.dim == 2:
            sphere = pathes.Circle(self.center, self.r, fill=False, color=color)
            axes.add_patch(sphere)
            del sphere
            return True
        elif self.dim == 3:
            u = np.linspace(0, 2 * np.pi, 100)
            v = np.linspace(0, np.pi, 100)

            x = np.subtract(self.r * np.outer(np.cos(u), np.sin(v)), -self.center[0])
            y = np.subtract(self.r * np.outer(np.sin(u), np.sin(v)), -self.center[1])
            z = np.subtract(self.r * np.outer(np.ones(np.size(u)), np.cos(v)), -self.center[2])
            print('x = ')
            print(x)
            print('y = ')
            print(y)

            axes.plot_surface(x, y, z, rstride=4, cstride=4, color=color, alpha=alpha)
            return True

        raise AttributeError("Defined only dor dimension 2 and 3")

    def find_intersection_with_surface(self, ray: Ray):
        # ���������� ��� �������� ������ ����� � ����� ���������(�� ��� ����� ������ �����)
        r0_p0 = np.subtract(self.center, ray.start)
        r0_p0e = np.dot(r0_p0, ray.dir)
        # ���� ������������
        disc = r0_p0e ** 2 - np.dot(r0_p0, r0_p0) + self.r ** 2
        if (abs(disc) < np.finfo(float).eps):
            disc = 0

        if disc < 0:
            print('no points of intersection ray %s with the sphere %s' % (str(ray), self.__str__()))
            return
        # ���� �����/������
        t = None
        if (disc != 0):
            sqrt_disc = m.sqrt(disc)
            t = [r0_p0e - sqrt_disc, r0_p0e + sqrt_disc]
        else:
            t = [r0_p0e]

        # ��������
        if all([i < 0 for i in t]):
            print('no points of intersection ray %s with the sphere %s' % (str(ray), self.__str__()))
            return
        # ������ ������������� ������
        positive_t = []
        for i in t:
            if i > np.finfo(float).eps:
                positive_t.append(i)
        if len(positive_t) > 0:
            return [ray.calc_point_of_ray(length) for length in positive_t]

    def find_nearest_point_intersection(self, ray: Ray):
        l = self.find_intersection_with_surface(ray)
        if l != None and len(l) > 0:
            return l[0]

    def is_point_belong(self, point: list) -> bool:
        if len(point) != self.dim:
            raise AttributeError("The point %s have different dimension than sphere(%s)" % (str(point), str(self.dim)))

        r0 = np.subtract(point, self.center)
        if abs(np.linalg.norm(r0) - self.r) < 10 * np.finfo(float).eps:
            return True

    def norm_vec(self, point):
        if not self.is_point_belong(point):
            raise AttributeError("The point %s is not belong surface %s" % (str(point), str(self)))

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
            return self.__n1, self.__n2
        return self.__n2, self.__n1
