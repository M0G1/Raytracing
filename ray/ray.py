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

    # methods of object ray====================================================================

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

    def calc_point_of_ray(self, t: float) -> list:
        if not t > 10 * np.finfo(float).eps:
            return
        point = []
        for i in range(self.__dim):
            point.append(self.__start[i] + self.__dir[i] * t)
        return point

    def _reflect(self, surface: Surface):
        if self.__dim != surface.dim:
            raise AttributeError("Different dimension of ray(%d) and of surface(%d)" % (self.__dim, surface.dim))
        # ШАГ-1 ищем точку
        point = surface.find_nearest_point_intersection(self)
        if point == None:
            return
        # ШАГ-2 ищем вектор нормали к поверхности
        nrm = surface.norm_vec(point)
        # проверяем на на нужное направление нормального вектора
        # e__1 = np.dot(-1.0, self.dir)
        # if (np.dot(nrm, e__1) < 0):
        #     nrm = np.dot(-1.0, nrm)
        # ШАГ-3 отражаем луч
        e_n = 2 * np.dot(self.dir, nrm)
        e = np.subtract(self.dir, np.dot(e_n, nrm))
        e = np.dot(1 / np.linalg.norm(e), e)
        # print("surf" + str(surface))
        # print("nrm" + str(nrm))
        # print("e" + str(e))
        return Ray(point, list(e))

    def _refract(self, surface: Surface):
        if self.__dim != surface.dim:
            raise AttributeError("Different dimension of ray(%d) and of surface(%d)" % (self.__dim, surface.dim))
        point = surface.find_nearest_point_intersection(self)

        if point == None:
            return

        # ШАГ-2 ищем вектор нормали к поверхности
        nrm = None
        # если точки пересечения две найдем два вектора нормали, а если одна то одну
        nrm = surface.norm_vec(point)
        # проверяем на на нужное направление нормального вектора
        e__1 = np.dot(-1.0, self.dir)
        if (np.dot(nrm, e__1) < 0):
            nrm = np.dot(-1.0, nrm)
        # ШАГ-3 преломляем луч
        n1, n2 = surface.get_refractive_indexes(self.start)
        # calc the formula of refraction
        v1 = np.dot(n1, self.dir)
        v1n = np.dot(v1, nrm)
        # print("n1,n2 = %d,%d" %(n1, n2))
        # print("nrm = %s" %(str(nrm)))
        # print("v1 = %s" %(str(v1)))
        # print("v1n = %s" %(str(v1n)))
        expression = 1 + (n2 ** 2 - n1 ** 2) / (v1n ** 2)
        # print('expression' + str(expression))
        if expression < 0:
            return self._reflect(surface)
        k = (m.sqrt(expression) - 1) * v1n
        e = np.dot(1 / n2, v1 + np.dot(k, nrm))

        return Ray(point, list(e))

    def is_total_returnal_refruction(self, surface: Surface) -> bool:
        point = surface.find_nearest_point_intersection(self)
        if point == None:
            return False
        # ШАГ-2 ищем вектор нормали к поверхности
        nrm = None
        # если точки пересечения две найдем два вектора нормали, а если одна то одну
        nrm = surface.norm_vec(point)
        # проверяем на на нужное направление нормального вектора
        e__1 = np.dot(-1.0, self.dir)
        if (np.dot(nrm, e__1) < 0):
            nrm = np.dot(-1.0, nrm)
        # ШАГ-3 преломляем луч
        n1, n2 = surface.get_refractive_indexes(self.start)
        # calc the formula of refraction
        v1 = np.dot(n1, self.dir)
        v1n = np.dot(v1, nrm)
        # print("n1,n2 = %d,%d" %(n1, n2))
        # print("nrm = %s" %(str(nrm)))
        # print("v1 = %s" %(str(v1)))
        # print("v1n = %s" %(str(v1n)))
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
                if point == None:
                    continue
                print("point in m_p" + str(point))
                norm_val = np.linalg.norm(np.subtract(self.start, point))
                if norm_val < min_p:
                    min_p = norm_val
                    index = i
                    i_point = point
            if i_point == None:
                break
            new_ray = None
            # смотрим характер поверхности t - True пропускает через себя свет, f - False не пропускает
            print("Surf  " + str(surfaces[index]))
            if surfaces[index].type == Surface.types.REFLECTING:
                new_ray = self._reflect(surfaces[index])
            elif surfaces[index].type == Surface.types.REFRACTING:
                new_ray = self._refract(surfaces[index])

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
