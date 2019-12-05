from enum import IntEnum
import numpy as np

from ray.ray import Ray
from surfaces.surface import Surface


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
        inequality = dim - cls.DIM
        cls.R_OFFSET.value += inequality
        cls.T0_OFFSET.value += inequality
        cls.T1_OFFSET.value += inequality
        cls.RAY_OFFSET.value += inequality
        cls.DIM = dim


class RaysPool:

    @staticmethod
    def __check_list(lst: list):
        if (len(lst) % Compon.RAY_OFFSET.value) != 0:
            raise AttributeError("Invalid length of rays list(%s)" % (str(len(lst))))
        RaysPool.__check_type(lst)

    @staticmethod
    def __check_type(lst):
        if not all(isinstance(i, (float, int)) or (i is None) for i in lst):
            raise TypeError("vector of direction and radius vector must consist from float or integer number")

    def __check_index(self, index: int):
        if index < 0 or index >= self.__rays_num:
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
        self.__check_list(rays)
        self.__pool = list(rays.copy())
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
        RaysPool.__check_list(rays)
        # extends list, appending at end of list all element from current list
        self.__pool.extend(rays)

        old_size = self.__rays_num
        self.refresh___rays_num()
        for num_ray in range(old_size, self.__rays_num):
            self.normalise_e(num_ray)

    def refresh___rays_num(self):
        val = len(self.__pool) / Compon.RAY_OFFSET.value
        if not isinstance(val, int):
            raise ValueError("ray number is not instance of integer(%s)".format(str(val.__class__.__name__)))
        self.__rays_num = val

    def erase_ray(self, index: int):
        RaysPool.__check_index(self, index)

        from_index = index * Compon.RAY_OFFSET.value
        # part of ray will shift to the left
        until_index = (self.__rays_num - 1) * Compon.RAY_OFFSET.value
        # shift on the deleting ray
        for i in range(from_index, until_index):
            self.__pool[i] = self.__pool[i + Compon.RAY_OFFSET.value]
        # delete last ray
        for i in range(Compon.RAY_OFFSET.value):
            # delete element at the end of list or on index - list.pop(index)
            self.__pool.pop()
        RaysPool.refresh___rays_num(self)

    # ================================================Magic methods=================================================

    def __str__(self):
        s = 'rays pool:\n'

        for i in range(self.__rays_num):
            s += ('%s- %s: %-60s, %s: %-60s, %s: %-18s, %s: %-18s\n'
                  % (str(i),
                     str(Compon.E_OFFSET), str(self.e(i)),
                     str(Compon.R_OFFSET), str(self.r(i)),
                     str(Compon.T0_OFFSET), str(self.t0(i)),
                     str(Compon.T1_OFFSET), str(self.t1(i)))
                  )
        return s

    def __len__(self):
        return self.__rays_num

    # ================================================Getters=================================================

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

    # ================================================Setters=================================================

    # calculate from radius vector of ray
    def set_t1(self, i: int, t1: float):
        if t1 < 0:
            raise AttributeError("Negative lenght(%f)" % (t1))
        if t1 < self.t0(i):
            raise AttributeError("Length less than begin of ray t0(%f), t1(%f)" % (self.t0(i), t1))
        r_i = i * Compon.RAY_OFFSET.value
        self.__pool[r_i + Compon.T1_OFFSET.value] = t1

    # methods of object RaysPool========================================================================================
    @staticmethod
    def __reflect_refract(func):
        # обертываем функцию
        def f(self, surface: Surface, push_non_reflected_ray: bool = True):
            rays = []
            # для заполения ячеек, куда мы не можем положить информацию (вычитаем два вектора e и r и начало)
            remain_len = Compon.RAY_OFFSET.value - (2 * Compon.DIM.value + 1)
            empty_list = [None for i in range(remain_len)]
            # моделируем отражние
            for i in range(len(self)):
                e, r, t1 = func(self.e(i), self.r(i), surface)
                if len(e) == 0 or len(r) == 0 or t1 is None:
                    if push_non_reflected_ray:
                        from_index = i * Compon.RAY_OFFSET.value
                        to_index = from_index + Compon.RAY_OFFSET.value
                        rays.extend(self.__pool[from_index:to_index])
                    else:
                        continue
                else:
                    self.set_t1(i, t1[0])
                    rays.extend(e)
                    rays.extend(r)
                    rays.append(0)
                    rays.extend(empty_list)

            return RaysPool(rays)

        return f

    def reflect(self, surface: Surface, push_non_reflected_ray: bool = True):
        ray_pool_reflect = RaysPool.__reflect_refract(Ray._reflect)
        return ray_pool_reflect(self, surface, push_non_reflected_ray)

    def refract(self, surface: Surface, push_non_refracted_ray: bool = True):
        ray_pool_reflect = RaysPool.__reflect_refract(Ray._refract)
        return ray_pool_reflect(self, surface, push_non_refracted_ray)
