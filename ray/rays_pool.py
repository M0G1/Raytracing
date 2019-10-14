from enum import IntEnum
import numpy as np


class Compon(IntEnum):
    """
    Component of RAY
    """
    E_OFFSET = 0
    R_OFFSET = 3
    T0_OFFSET = 6
    T1_OFFSET = 7
    # For future code
    # LAM_OFFSET.value = 8
    # W_OFFSET.value = 9
    RAY_OFFSET = 8
    DIM = 3

    @classmethod
    def new_dimension(cls, dim: int):
        if dim < 1:
            raise AttributeError("Dimension too small(%s)" % (str(dim)))
        cls.R_OFFSET.value = dim
        cls.T0_OFFSET.value = cls.R_OFFSET.value + dim
        cls.T1_OFFSET.value = cls.T0_OFFSET.value + 1
        cls.RAY_OFFSET.value = cls.T1_OFFSET.value + 1
        cls.DIM = dim


class RaysPool:

    def __init__(self, rays: list):
        if (len(rays) % Compon.RAY_OFFSET.value) != 0:
            raise AttributeError("Invalid length of rays list(%s)" % (str(len(rays))))
        if not all(isinstance(i, float) or isinstance(i, int) for i in rays):
            raise TypeError("Array must consist from float")
        self.__pool = rays.copy()
        self.__rays_num = len(rays) // Compon.RAY_OFFSET.value
        
        # normalisation of direction vector
        for i in range(self.__rays_num):
            norm_val = np.linalg.norm(self.e(i))
            if abs(norm_val - 1) > np.finfo(float).eps:
                r_i = i * Compon.RAY_OFFSET.value
                for i in range(r_i, r_i + Compon.DIM.value):
                    self.__pool[i] /= norm_val

    @property
    def rays_number(self):
        return self.__rays_num

    def e(self, i: int):
        r_i = i * Compon.RAY_OFFSET.value
        a = r_i + Compon.E_OFFSET.value
        b = r_i + Compon.R_OFFSET.value
        return self.__pool[a:b]

    def r(self, i: int):
        r_i = i * Compon.RAY_OFFSET.value
        a = r_i + Compon.R_OFFSET.value
        b = r_i + Compon.T0_OFFSET.value
        return self.__pool[a:b]

    def t0(self, i: int) -> float:
        r_i = i * Compon.RAY_OFFSET.value
        return self.__pool[r_i + Compon.T0_OFFSET.value]

    def t1(self, i) -> float:
        r_i = i * Compon.RAY_OFFSET.value
        return self.__pool[r_i + Compon.T1_OFFSET.value]
