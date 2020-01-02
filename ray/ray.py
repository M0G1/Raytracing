import numpy as np
import pylab

from surfaces.surface import Surface
import controllers.rayController as rsc
import math as m
from utility.binarytree import Tree


class Ray:
    # Конструктор класса Ray, создает объекты лучей из двух массивов вещественных числел
    # начала луча(start) и направление(dirrection)
    def __init__(self, start: list, direction: list, amplitude: float = 1):
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
            self.__amplitude = amplitude
            self.__path_of_ray = []
            self.__t1 = np.iinfo(int).max
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
    def t1(self) -> float:
        return self.__t1

    @property
    def A(self) -> float:
        return self.__amplitude

    @A.setter
    def A(self, amplitude: (float, int)):
        if amplitude > 0:
            self.__amplitude = amplitude

    @t1.setter
    def t1(self, t1_: (float, int)):
        if t1_ > 0:
            self.__t1 = t1_

    # methods of object ray===========================================================================================

    def __str__(self) -> str:
        return "ray:{ start: %s, direction: %s}" % (self.__start.__str__(), self.__dir.__str__())

    def reflect(self, surface: Surface):
        if self.__dim != surface.dim:
            raise AttributeError("Different dimension of ray(%d) and of surface(%d)" % (self.__dim, surface.dim))
        point, e, t_1 = rsc.reflect(e=self.dir, r=self.start, surface=surface)
        if len(point) == 0 or len(e) == 0 or t_1 is None:
            return None
        self.t1 = t_1
        return Ray(point, e)

    def refract(self, surface: Surface):
        if self.__dim != surface.dim:
            raise AttributeError("Different dimension of ray(%d) and of surface(%d)" % (self.__dim, surface.dim))
        # list, list, float
        point, e, t_1 = rsc.refract(e=self.dir, r=self.start, surface=surface)
        if len(point) == 0 or len(e) == 0 or t_1 is None:
            return None
        self.t1 = t_1
        return Ray(point, e)

    def calc_point_of_ray(self, t: float) -> list:
        if not t > 10 * np.finfo(float).eps:
            return []
        return rsc.calc_point_of_ray_(self.dir, self.start, t)
