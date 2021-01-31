from enum import Enum
from typing import TypeVar, Union, List, Tuple
import numpy as np

from surfaces.additional.polar_mat import PolarMat

T = TypeVar("T")


class Types(Enum):
    REFLECTING = 1
    REFRACTING = 2
    POLARIZING = 3


class Surface:
    """
    The class interface for describing some surface in space.
    The surface have a type. See enumerate Surface.types. The type define the behaviour of modeling methods(raytracing).
    The surface define in some space, what there is having a dimension.

    Surface must have defined next function
    "norm_vec" - normal vector to some point in space.
    "get_refractive_indexes" - getting a refractive indexes to some point in space.
    find the intersection with surface - get the length of ray, where point on ray intersect the surface:
        "_ray_surface_intersection"  - get for abstract ray presented as vector of direction and start point


    """
    types = Types

    # __dim = 0

    #  Don't usable in logic of program
    def __init__(self, type_of_surface: Types, dimension: int, polarisation_matrix_refract: PolarMat = None,
                 polarisation_matrix_reflect: PolarMat = None):
        """
        :param type_of_surface Param contains the type of surface. There is the following hierarchy
        - REFLECTING, REFRACTING, POLARIZING.
        Creation of few rays must be realized by modeling function(method).
        :param dimension : The dimension of space where define surface
        :param polarisation_matrix_refract : Polarisation matrix for refracted ray case.
        :param polarisation_matrix_reflect : Polarisation matrix for reflected ray case.
        """
        self.__type_of_surface = type_of_surface
        self.__dim = dimension
        self.__polar_mat_refract = polarisation_matrix_refract
        self.__polar_mat_reflect = polarisation_matrix_reflect

        self._check_polarisation_matrix()

    # ========================================= Check Methods ==========================================================

    def _check_polarisation_matrix(self):
        if self.__polar_mat_reflect is None and self.__type_of_surface == Surface.types.POLARIZING:
            self.__polar_mat_reflect = PolarMat()
        if self.__polar_mat_refract is None and self.__type_of_surface == Surface.types.POLARIZING:
            self.__polar_mat_refract = PolarMat()

    # ========================================= Getter Setter ==========================================================

    @property
    def type(self):
        return self.__type_of_surface

    @property
    def dim(self):
        return self.__dim

    @property
    def polar_matrix_refract(self):
        return self.__polar_mat_refract

    @polar_matrix_refract.setter
    def polar_matrix_refract(self, value: PolarMat):
        self.__polar_mat_refract = value

    @property
    def polar_matrix_relect(self):
        return self.__polar_mat_reflect

    @polar_matrix_relect.setter
    def polar_matrix_relect(self, value: PolarMat):
        self.__polar_mat_reflect = value

    # =================================== Surface object  methods ======================================================
    def is_point_belong(self, point: [List[Union[float, int]], np.ndarray]) -> bool:
        pass

    def norm_vec(self, point: [List[Union[float, int]], np.ndarray]) -> \
            Union[List[Union[float, int]], np.ndarray, None]:
        """
        :param point: point in space
        :return: normal vector of real number for given point
        """
        return

    def get_refractive_indexes(self, point: [List[Union[float, int]], np.ndarray]):
        """
        Any surface divides the space into 2 parts.

        Coefficient n1 corresponds to the external one (for surfaces bounding the space)
        or on the opposite side relative to the normal plane vector

        Coefficient n2 corresponds to the inside (for surfaces bounding the space)
        or on the same side relative to the normal plane vector
        :param point: point in space
        :return: list of refracted indexes where first is refracted index for given point
        """
        pass

    def set_refractive_indexes(self, n1: (float, int) = 1, n2: (float, int) = 1):
        if n1 < 1 or n2 < 1:
            raise AttributeError("Refractive indices less than unity. n1: {}, n2: {}".format(n1, n2))
        self.__n1 = n1
        self.__n2 = n2

    # def draw_surface(self, axes) -> bool:
    #     return False

    # ======================================= methods for Ray ==========================================================

    def _ray_surface_intersection(self, e: [List[Union[float, int]], np.ndarray],
                                  r: [List[Union[float, int]], np.ndarray]) \
            -> Union[List[Union[float, int]], np.ndarray, None]:
        """Get for abstract ray presented as vector of direction and start point
        :param e vector of direction of ray.
        :param r starting point of ray
        :return: get the length of ray, where point on ray intersect the surface
        """

    pass

    def find_intersection_with_surface(self, ray) -> Union[List[Union[float, int]], np.ndarray, None]:
        """Get for ray presented as class of 1 ray.
        The length of ray must be sorted by increase
        :param ray object of class Ray. (see ray.ray.py)
        :return: get the lengths of ray, where point on ray intersect the surface
        """
        pass

    def find_nearest_point_intersection(self, ray):
        """Get for ray presented as class of 1 ray
        :param ray object of class Ray. (see ray.ray.py)
        :return: get the length of ray, where point on ray of nearest intersection with surface
        """
        ret_res = self.find_intersection_with_surface(ray)
        return ret_res[0] if ret_res is not None else None

    # ======================================== methods for Ray_pool ====================================================
    def find_intersection_pool_with_surface(self, pool, index: int) -> Union[List[Union[float, int]], np.ndarray, None]:
        pass

    def find_nearest_intersection_pool_with_surface(self, pool, index: int) \
            -> Union[List[Union[float, int]], np.ndarray, None]:
        pass
