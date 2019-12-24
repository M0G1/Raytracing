import numpy as np
import pylab

from surfaces.surface import Surface
import math as m
from utility.binarytree import Tree


class Ray:
    # Конструктор класса Ray, создает объекты лучей из двух массивов вещественных числел
    # начала луча(start) и направление(dirrection)
    def __init__(self, start: list, direction: list):
        if len(direction) == len(start):
            if not all(isinstance(i, float or int) and isinstance(j, float or int) for i, j in zip(start, direction)):
                raise AttributeError(
                    """Some element in %s or %s is not a float number..""" % (str(start), str(direction)))

            self.__dir = direction.copy()
            norm_val = np.linalg.norm(self.dir)
            if abs(norm_val - 1.0) > np.finfo(float).eps:
                self.__dir = np.dot(1 / norm_val, self.dir)
            self.__dim = len(direction)
            self.__start = start.copy()
            self.__path_of_ray = []
            self.__t1 = [np.iinfo(int).max, None]
        else:
            raise AttributeError("""Iterables objects have different length. 
        len(start): %d,
        len(direction): %d""" % (len(start), len(direction)))

    # getter and setter====================================================================

    @property
    def dim(self):
        return self.__dim

    @property
    def dir(self) -> list:
        return self.__dir.copy()

    @property
    def start(self) -> list:
        return self.__start.copy()

    @property
    def t1(self) -> list:
        return self.__t1

    @t1.setter
    def t1(self, t1_: list):
        if len(t1_) != 2:
            raise AttributeError("t1 must be list from 2 object(%d)" % (len(t1_)))
        if self.__t1[0] > t1_[0]:
            self.__t1 = t1_

    # static methods of ray====================================================================

    @staticmethod
    def calc_point_of_ray_(e: list, r: list, t: float) -> list:
        return list(np.add(np.multiply(t, e), r))

    @staticmethod
    def _find_norm_vec_and_point(e: list, r: list, surface: Surface):
        # Шаг-1 ищем точку пересечения
        t = surface._ray_surface_intersection(e, r)
        if len(t) == 0:
            return [], [], None
        point = Ray.calc_point_of_ray_(e, r, t[0])
        # ШАГ-2 ищем вектор нормали к поверхности
        nrm = surface.norm_vec(point)
        if nrm is None:
            return [], [], None
        return point, nrm, t

    @staticmethod
    def _refract(e: list, r: list, surface: Surface):
        point, nrm, t = Ray._find_norm_vec_and_point(e, r, surface)
        if len(point) == 0 and len(nrm) == 0 and t is None:
            return [], [], None
        # ШАГ-3 преломляем луч
        n1, n2 = surface.get_refractive_indexes(r)
        # calc the formula of refraction
        v1 = np.dot(n1, e)
        v1n = np.dot(v1, nrm)
        expression = 1 + (n2 ** 2 - n1 ** 2) / (v1n ** 2)
        if expression < 0:
            return Ray._reflect(e, r, surface)
        k = (m.sqrt(expression) - 1) * v1n
        e = np.dot(1 / n2, v1 + np.dot(k, nrm))
        return list(point), list(e), t[0]

    @staticmethod
    def _reflect(e: list, r: list, surface: Surface):
        point, nrm, t = Ray._find_norm_vec_and_point(e, r, surface)
        if len(point) == 0 and len(nrm) == 0 and t is None:
            return [], [], None
        # ШАГ-3 отражаем луч
        e_n = 2 * np.dot(e, nrm)
        e = np.subtract(e, np.dot(e_n, nrm))
        e = np.dot(1 / np.linalg.norm(e), e)
        return list(point), list(e), t[0]

    # methods of object ray=============================================================================================

    def __str__(self) -> str:
        return "ray:{ start: %s, direction: %s}" % (self.__start.__str__(), self.__dir.__str__())

    def __append_point_to_path(self, way_points_of_ray: list, point: list):
        if len(point) == 0:
            raise AttributeError("Zero dimensional point")
        if len(way_points_of_ray) != 0 and (len(point) != len(way_points_of_ray) or self.dim != len(point)):
            raise AttributeError(
                "Iterables objects(point) have different length with ray or way_points_of_ray. len(way_points_of_ray): %d, len(point): %d, ray(%d)" % (
                    len(way_points_of_ray), len(point), self.dim))
        if len(way_points_of_ray) == 0:
            for i in range(self.dim):
                way_points_of_ray.append([])
            for j in range(self.__dim):
                way_points_of_ray[j].append(self.start[j])
        for j in range(self.__dim):
            way_points_of_ray[j].append(point[j])

    def reflect(self, surface: Surface):
        if self.__dim != surface.dim:
            raise AttributeError("Different dimension of ray(%d) and of surface(%d)" % (self.__dim, surface.dim))
        point, e, t_1 = Ray._reflect(e=self.dir, r=self.start, surface=surface)
        if len(point) == 0 or len(e) == 0 or t_1 is None:
            return None
        self.t1 = [t_1, surface]
        return Ray(point, e)

    def refract(self, surface: Surface):
        if self.__dim != surface.dim:
            raise AttributeError("Different dimension of ray(%d) and of surface(%d)" % (self.__dim, surface.dim))
        # list, list, float
        point, e, t_1 = Ray._refract(e=self.dir, r=self.start, surface=surface)
        if len(point) == 0 or len(e) == 0 or t_1 is None:
            return None
        self.t1 = [t_1, surface]
        return Ray(point, e)

    def calc_point_of_ray(self, t: float) -> list:
        if not t > 10 * np.finfo(float).eps:
            return []
        return Ray.calc_point_of_ray_(self.dir, self.start, t)

    def is_total_returnal_refraction(self, surface: Surface) -> bool:
        # list, list, float
        point, nrm, t_1 = Ray._find_norm_vec_and_point(self.dir, self.start, surface)
        if len(point) == 0 and len(nrm) == 0 and t_1 is None:
            return False
        self.t1 = [t_1, surface]
        # ШАГ-3 преломляем луч
        n1, n2 = surface.get_refractive_indexes(self.start)
        # calc the formula of refraction
        v1 = np.dot(n1, self.dir)
        v1n = np.dot(v1, nrm)
        expression = 1 + (n2 ** 2 - n1 ** 2) / (v1n ** 2)
        return expression < 0

    def _model_path(self, surfaces: list) -> list:
        way_point_of_ray = []
        while True:
            min_p = float(np.finfo(float).max)
            # index of nearest surface and intersection point
            index, i_point = -1, None
            # ищем ближайшую поверхность
            for i in range(len(surfaces)):
                point = None
                point = surfaces[i].find_nearest_point_intersection(self)
                print("point in m_p" + str(point))
                if (point == None) or (len(point) == 0):
                    continue
                print('point is not null '+ str(point == None))
                print('start of ray' + str(self.start))
                norm_val = np.linalg.norm(np.subtract(self.start, point))
                if norm_val < min_p:
                    min_p = norm_val
                    index = i
                    i_point = point
            if i_point == None:
                break
            new_ray = None
            # print("Surf  " + str(surfaces[index]))
            if surfaces[index].type == Surface.types.REFLECTING:
                new_ray = self.reflect(surfaces[index])
            elif surfaces[index].type == Surface.types.REFRACTING:
                new_ray = self.refract(surfaces[index])

            if new_ray != None:
                self.__append_point_to_path(way_point_of_ray, new_ray.start)
                self.__dir = new_ray.dir
                self.__start = new_ray.start
                del new_ray
        return way_point_of_ray

    def path_ray(self, surfaces: list) -> list:
        if not all(isinstance(some, Surface) for some in surfaces):
            raise AttributeError(
                "Not all elements in surfaces is instance of class Surface %s" % (
                    str([type(some) for some in surfaces]))
            )
        self.__path_of_ray = self._model_path(surfaces)
        ans = self.__path_of_ray.copy()
        self.__append_point_to_path(ans, self.calc_point_of_ray(100_000))
        return ans

    def draw_ray(self, axes, way_points_of_ray: list, color="green"):
        if len(way_points_of_ray) == 2:
            axes.add_line(pylab.Line2D(way_points_of_ray[0], way_points_of_ray[1], color=color, marker=''))
        if len(way_points_of_ray) == 3:
            axes.plot(
                way_points_of_ray[0],
                way_points_of_ray[1],
                way_points_of_ray[2],
                label='LINE', color=color);
            axes.scatter(way_points_of_ray[0],
                         way_points_of_ray[1],
                         way_points_of_ray[2],
                         c='b', marker='o')
