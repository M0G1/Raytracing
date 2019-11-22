import numpy as np
import pylab
from enum import Enum


class Types(Enum):
    REFLECTING = 1
    REFRACTING = 2


class Surface:
    types = Types
    __type_of_surface = types.REFLECTING
    # __dim = 0

    #  Don't usable in logic of program
    # def __init__(self, type_of_surface: bool, dimension: int):
    #     self.__type_of_surface = type_of_surface
    #     self.__dim = dimension

    @property
    def type(self):
        return self.__type_of_surface

    @property
    def dim(self):
        return self.__dim

    # =================================== Surface object  methods ======================================================
    def is_point_belong(self, point: list) -> bool:
        pass

    def norm_vec(self, point)->list:
        return

    def get_refractive_indexes(self, point: list):
        """
        Any surface divides the space into 2 parts.

        Coefficient n1 corresponds to an external(for space-bounding surfaces)
        or lower(opposite to the direction of most normal vectors to this surface).

        Coefficient 2 corresponds to the inside(for the surfaces bounding the space)
        or the top (co-directional in the direction of most normal vectors to this surface).
        :param point:
        :return:
        """
        pass

    def draw_surface(self, axes) -> bool:
        return False

    # ======================================= methods for Ray ==========================================================
    def find_intersection_with_surface(self, ray):
        pass

    def find_nearest_point_intersection(self, ray):
        pass

    # ======================================== methods for Ray_pool ====================================================
    def find_intersection_pool_with_surface(self, pool, index: int) -> list:
        pass

    def find_nearest_intersection_pool_with_surface(self, pool, index: int)->list:
        pass
