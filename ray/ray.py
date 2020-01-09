import numpy as np
import pylab

from surfaces.surface import Surface
import controllers.rayStaticController as rsCTRL
import math as m
from utility.binarytree import Tree


class Ray:
    EPS0 = 1 / (4 * np.pi * 9 * 10 ** 9)
    nu0 = 4 * np.pi * 10 ** -7
    SQRT_EPS0_ON_NU0 = (EPS0 / nu0) ** 0.5

    # Конструктор класса Ray, создает объекты лучей из двух массивов вещественных числел
    # начала луча(start) и направление(dirrection)
    def __init__(self, start: list, direction: list, amplitude: float = 1, brightness: float = 1):
        if len(direction) == len(start):
            if not all(isinstance(i, float or int) and isinstance(j, float or int) for i, j in zip(start, direction)):
                raise AttributeError(
                    """Some element in %s or %s is not a float number..""" % (str(start), str(direction)))
            if amplitude <= 0:
                raise AttributeError("Amplitude must be positive digit(%s)" % (str(amplitude)))
            if brightness <= 0 or brightness > 1:
                raise AttributeError(
                    "Brightness must be positive digit more than zero and less than one(%s)" % (str(brightness)))

            self.__dir = direction.copy()
            norm_val = np.linalg.norm(self.dir)
            if abs(norm_val - 1.0) > np.finfo(float).eps:
                self.__dir = np.dot(1 / norm_val, self.dir)
            self.__dim = len(direction)
            self.__start = start.copy()
            self.__amplitude = amplitude
            self.__brightness = brightness
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

    @property
    def bright(self) -> float:
        return self.__brightness

    @t1.setter
    def t1(self, t1_: (float, int)):
        if t1_ > 0:
            self.__t1 = t1_

    @A.setter
    def A(self, amplitude: (float, int)):
        if amplitude <= 0:
            raise AttributeError("Amplitude must be positive digit(%s)" % (str(amplitude)))
        self.__amplitude = amplitude

    @bright.setter
    def bright(self, brightness):
        if brightness <= 0 or brightness > 1:
            raise AttributeError(
                "Brightness must be positive digit more than zero and less than one(%s)" % (str(brightness)))
        self.__brightness = brightness

    # methods of object ray===========================================================================================

    def __str__(self) -> str:
        return "ray:{ start: %s, direction: %s, A: %s, B:%s}" % (
        self.__start.__str__(), self.__dir.__str__(), str(self.A), str(self.bright))

    def reflect(self, surface: Surface):
        if self.__dim != surface.dim:
            raise AttributeError("Different dimension of ray(%d) and of surface(%d)" % (self.__dim, surface.dim))
        point, e, t_1 = rsCTRL.reflect(e=self.dir, r=self.start, surface=surface)
        if len(point) == 0 or len(e) == 0 or t_1 is None:
            return None
        self.t1 = t_1
        return Ray(point, e)

    def refract(self, surface: Surface):
        if self.__dim != surface.dim:
            raise AttributeError("Different dimension of ray(%d) and of surface(%d)" % (self.__dim, surface.dim))
        # list, list, float
        point, e, t_1 = rsCTRL.refract(e=self.dir, r=self.start, surface=surface)
        if len(point) == 0 or len(e) == 0 or t_1 is None:
            return None
        self.t1 = t_1
        return Ray(point, e)

    def calc_point_of_ray(self, t: float) -> list:
        if not t > 10 * np.finfo(float).eps:
            return []
        return rsCTRL.calc_point_of_ray_(self.dir, self.start, t)

    def calc_I(self, n: float):
        return Ray.SQRT_EPS0_ON_NU0 * self.A ** 2
