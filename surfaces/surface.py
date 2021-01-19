from enum import Enum


class Types(Enum):
    REFLECTING = 1
    REFRACTING = 2
    POLARIZING = 3


class Surface:
    types = Types

    # __dim = 0

    #  Don't usable in logic of program
    def __init__(self, type_of_surface: Types, dimension: int):
        self.__type_of_surface = type_of_surface
        self.__dim = dimension
        self.__

    @property
    def type(self):
        return self.__type_of_surface

    @property
    def dim(self):
        return self.__dim

    # =================================== Surface object  methods ======================================================
    def is_point_belong(self, point: (list, tuple)) -> bool:
        pass

    def norm_vec(self, point) -> list:
        return

    def get_refractive_indexes(self, point: list):
        """
        Any surface divides the space into 2 parts.

        Coefficient n1 corresponds to the external one (for surfaces bounding the space)
        or on the opposite side relative to the normal plane vector

        Coefficient n2 corresponds to the inside (for surfaces bounding the space)
        or on the same side relative to the normal plane vector
        :param point:
        :return:
        """
        pass

    def set_refractive_indexes(self, n1: float = 1, n2: float = 1):
        if n1 < 1 or n2 < 1:
            raise AttributeError("Refractive indices less than unity. n1: {}, n2: {}".format(n1, n2))
        self.__n1 = n1
        self.__n2 = n2

    # def draw_surface(self, axes) -> bool:
    #     return False

    # ======================================= methods for Ray ==========================================================

    def _ray_surface_intersection(self, e: list, r: list) -> list:
        pass

    def find_intersection_with_surface(self, ray):
        pass

    def find_nearest_point_intersection(self, ray):
        pass

    # ======================================== methods for Ray_pool ====================================================
    def find_intersection_pool_with_surface(self, pool, index: int) -> list:
        pass

    def find_nearest_intersection_pool_with_surface(self, pool, index: int) -> list:
        pass
