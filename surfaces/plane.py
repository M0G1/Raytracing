from surfaces.surface import Surface
from ray.ray import Ray
import numpy as np
import pylab
import matplotlib.lines as mlines


class Plane(Surface):
    __rad = ()
    __norm = ()

    def __init__(self, radius_vector: list, normal_vector: list,
                 type_surface: Surface.types = Surface.types.REFLECTING,
                 n1: float = 1,
                 n2: float = 1):
        if len(normal_vector) != len(radius_vector):
            raise AttributeError("""Iterables objects have different length. 
                           len(radius_vector): %d,
                           len(normal_vector): %d""" % (len(radius_vector), len(normal_vector)))
        if n1 < 1. or n2 < 1.:
            raise AttributeError("Refractive indices less than unity. n1: {}, n2: {}".format(n1, n2))
        if not all(isinstance(i, int) or
                   isinstance(j, int) or
                   isinstance(i, float) or
                   isinstance(j, float) for i, j in zip(radius_vector, normal_vector)):
            raise AttributeError(
                """Some element in %s or %s is not a float number.""" % (
                    str(radius_vector), str(normal_vector)))

        self._Surface__dim = len(radius_vector)
        self._Surface____type_of_surface = type_surface
        self.__rad = radius_vector
        self.__norm = normal_vector
        norm_val = np.linalg.norm(self.__norm)
        if abs(norm_val - 1.0) > np.finfo(float).eps:
            self.__norm = np.dot(1 / norm_val, self.__norm)
        self.__n1 = n1
        self.__n2 = n2

    # getter and setter====================================================================

    @property
    def rad(self) -> list:
        return self.__rad

    # methods of object plane====================================================================

    def __str__(self):
        return "Plane{ radius_vector: %s, normal_vector: %s, type: %s}" % (
            str(self.rad), str(self.__norm), str(self.type))

    def draw_surface(self, axes: type(pylab.gca())) -> bool:
        if self.dim == 2:
            # matrix of rotation
            m = [[0, -1],
                 [1, 0]]
            # direction vector
            r = np.dot(m, self.__norm)

            def calc_point(start: list, dir, leng):
                poin = []
                for i in range(len(start)):
                    poin.append(start[i] + dir[i] * leng)
                return poin

            point = [calc_point(self.rad, r, 10_000),
                     calc_point(self.rad, r, -10_000)]
            line = mlines.Line2D([point[i][0] for i in range(2)],
                                 [point[i][1] for i in range(2)])
            axes.add_line(line)
            return True
        elif self.dim == 3:
            return False
        raise AttributeError("Defined only dor dimension 2 and 3")

    def find_intersection_with_surface(self, ray: Ray):
        ne = np.dot(ray.dir, self.__norm)
        if abs(ne) < np.finfo(float).eps:
            # here
            equal = True
            for i in range(3):
                if abs(ray.start[i] - self.rad[i]) > np.finfo(float).eps:
                    equal = False
                    break
            if equal:
                print("The beam %s lies on a plane %s " % (str(ray), self.__str__()))
            else:
                print("The beam %s is parallel to the plane %s" % (str(ray), self.__str__()))
            return
        t = (np.dot(self.__norm, np.subtract(self.__rad, ray.start))) / ne
        # проверка на пересечение плоскостью в нужном направлении???
        if t < 0:
            print("no intersection points ray %s with the plane %s " % (str(ray), self.__str__()))
            return
        return ray.calc_point_of_ray(t)

    def find_nearest_point_intersection(self, ray: Ray):
        return self.find_intersection_with_surface(ray)

    def is_point_belong(self, point: list) -> bool:
        if len(point) != self.dim:
            raise AttributeError("The point %s have different dimension than plane(%s)" % (str(point), str(self.dim)))

        r0 = np.subtract(point, self.rad)
        if abs(np.dot(r0, self.__norm)) < 10 * np.finfo(float).eps:
            return True

    def norm_vec(self, point: list):
        if not self.is_point_belong(point):
            raise AttributeError("The point %s is not belong surface %s" % (str(point), str(self)))
        return self.__norm

    def get_refractive_indexes(self, point: list):
        """
        returns 2 coefficients
        :param point:
        :return: n1,n2
        """
        """
        Any point returning n1 has an angle with a normal vector greater than 90 degrees.(Different directions)
        Any point returning n2 has an angle with a normal vector less than 90 degrees(for angle zero to).(Same direction)"""
        rad_vec = np.subtract(point, self.rad)
        cos_angle = np.dot(rad_vec, self.__norm)
        if cos_angle < -10 * np.finfo(float).eps:
            return self.__n1, self.__n2
        return self.__n2, self.__n1
