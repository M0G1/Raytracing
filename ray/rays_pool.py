from enum import Enum
import numpy as np


class Compon(Enum):
    """
    Component of RAY
    """
    E_OFFSET = 0
    R_OFFSET = 3
    T0_OFFSET = 6
    T1_OFFSET = 7
    # For future code
    # LAM_OFFSET = 8
    # W_OFFSET = 9
    RAY_OFFSET = 8
    DIM = 3

    @classmethod
    def new_dimension(cls, dim: int):
        if dim < 1:
            raise AttributeError("Dimension too small(%s)" % (str(dim)))
        cls.R_OFFSET = dim
        cls.T0_OFFSET = cls.R_OFFSET + dim
        cls.T1_OFFSET = cls.T0_OFFSET + 1
        cls.RAY_OFFSET = cls.T1_OFFSET + 1
        cls.DIM = dim


class RaysPool:

    def __init__(self, rays: list):
        if len(rays) // Compon.RAY_OFFSET != 0:
            raise AttributeError("Invalid length of rays list(%s)" % (str(len(rays))))
        self.__pool = rays.copy()
        norm_val = np.linalg.norm(rays[:Compon.R_OFFSET])
        if abs(norm_val - 1) > np.finfo(float).eps:
            for i in range(Compon.E_OFFSET, Compon.R_OFFSET):
                self.__pool[i] = self.__pool[i] / norm_val

    def e(self, i):
        a, b = i * Compon.RAY_OFFSET*(Compon.E_OFFSET, Compon.R_OFFSET)
        return self.__pool[a:b]

    def r(self, i):
        return self.__pool[Compon.R_OFFSET, Compon.T0_OFFSET]

    def t0(self, i):
        return self.__pool[Compon.T0_OFFSET]

    def t1(self, i):
        return self.__pool[Compon.T1_OFFSET]
