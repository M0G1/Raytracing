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

    @staticmethod
    def check_list(lst: list):
        if (len(lst) == 0) or (len(lst) % Compon.RAY_OFFSET.value) != 0:
            raise AttributeError("Invalid length of rays list(%s)" % (str(len(lst))))
        if not all(isinstance(i, float) or isinstance(i, int) for i in lst):
            raise TypeError("Array must consist from float or integer number")

    def check_index(self, index: int):
        if index < 0 or index >= self.rays_number:
            raise IndexError("Incorrect index(%s)" % (str(index)))

    # @staticmethod
    # def _calc_new_length(length: int) -> int:
    #     """
    #     adds 25 percent to the number of available offset lengths
    #     :param length:
    #     :return:
    #     """
    #     if (length * 0.25 // Compon.RAY_OFFSET.value) < 1:
    #         return length + Compon.RAY_OFFSET
    #     return (int(1.25 * length) // Compon.RAY_OFFSET.value) * Compon.RAY_OFFSET.value

    # ================================================Object's=================================================

    def __init__(self, rays: list):
        self.check_list(rays)
        self.__pool = rays.copy()
        self.__rays_num = len(rays) // Compon.RAY_OFFSET.value

        # normalisation of direction vector
        for i in range(self.__rays_num):
            self.normalise_e(i)

    def normalise_e(self, index: int):
        norm_val = np.linalg.norm(self.e(index))
        if abs(norm_val - 1) > np.finfo(float).eps:
            r_i = index * Compon.RAY_OFFSET.value
            for i in range(r_i, r_i + Compon.DIM.value):
                self.__pool[i] /= norm_val

    def append_rays(self, rays: list):
        RaysPool.check_list(rays)
        # extends list, appending at end of list all element from current list
        self.__pool.extend(rays)

        old_size = self.rays_number
        self.refresh_rays_number()
        for num_ray in range(old_size, self.rays_number):
            self.normalise_e(num_ray)

    def refresh_rays_number(self):
        self.__rays_num = len(self.__pool) // Compon.RAY_OFFSET.value

    def erase_ray(self, index: int):
        RaysPool.check_index(self, index)

        from_index = index * Compon.RAY_OFFSET.value
        # part of ray will shift to the left
        until_index = (self.rays_number - 1) * Compon.RAY_OFFSET.value
        # shift on the deleting ray
        for i in range(from_index, until_index):
            self.__pool[i] = self.__pool[i + Compon.RAY_OFFSET.value]
        # delete last ray
        for i in range(Compon.RAY_OFFSET.value):
            # delete element at the end of list or on index - list.pop(index)
            self.__pool.pop()
        RaysPool.refresh_rays_number(self, -1)

    def __str__(self):
        s = 'rays pool:\n'

        for i in range(self.rays_number):
            s += ('%s- %s: %-60s, %s: %-60s, %s: %-18s, %s: %-18s\n'
                  % (str(i),
                     str(Compon.E_OFFSET), str(self.e(i)),
                     str(Compon.R_OFFSET), str(self.r(i)),
                     str(Compon.T0_OFFSET), str(self.t0(i)),
                     str(Compon.T1_OFFSET), str(self.t1(i)))
                  )
        return s

    # ================================================Getters=================================================

    @property
    def rays_number(self):
        return self.__rays_num

    def e(self, i: int) -> list:
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
