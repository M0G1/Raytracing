from enum import IntEnum
import numpy as np

from ray.abstract_ray import ARay

from surfaces.surface import Surface


class Compon_Interface(IntEnum):
    pass


class Compon2D(Compon_Interface):
    """
        Component of 2 dimension RAY
    """

    E_OFFSET = 0
    R_OFFSET = 2
    T0_OFFSET = 4
    T1_OFFSET = 5
    l_OFFSET = 6
    # For future code
    # LAM_OFFSET.value = 6
    # W_OFFSET.value = 7
    RAY_OFFSET = 7
    DIM = 2


class Compon3D(Compon_Interface):
    """
        Component of  3 dimension  RAY
    """
    E_OFFSET = 0
    R_OFFSET = 3
    T0_OFFSET = 6
    T1_OFFSET = 7
    # l_OFFSET = 8
    # For future code
    # LAM_OFFSET.value = 8
    # W_OFFSET.value = 9
    RAY_OFFSET = 8
    DIM = 3


class RaysPool(ARay):
    """
        Class of set of rays. It have access methods: e,r,t0,t1
         and some data manipulating ones: reflect,refract.
    """

    @staticmethod
    def __check_type(lst):
        if not all(isinstance(i, (float, int)) or (i is None) for i in lst):
            raise TypeError("vector of direction and radius vector must consist from float or integer number")

    @staticmethod
    def __check_comIndex(componentIndexes):
        if not issubclass(componentIndexes, (Compon2D, Compon3D)):
            raise AttributeError("componentIndexes must be the class Compon2D or Compon3D." +
                                 " And you take %s" % str(componentIndexes))

    def __check_index(self, index: int):
        if index < 0 or index >= self.__rays_num:
            raise IndexError("Incorrect index(%s)" % (str(index)))

    def __check_list(self, lst: list):
        if (len(lst) % self.__ComIndex.RAY_OFFSET) != 0:
            raise AttributeError("Invalid length of rays list(%d). It must be multiplied  by %d" % (
                len(lst), self.__ComIndex.RAY_OFFSET))
        RaysPool.__check_type(lst)

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

    def __init__(self, rays: (list, iter), componentIndexes):
        """
        :param rays: iterable object with Numeric values. It is lenght must be a multiple value of RAY_OFFSET
         of class Compon2D or Compon3D
        :param componentIndexes: class Compon2D or Compon3D with needed dimension space
        """

        self.__check_comIndex(componentIndexes)
        self.__ComIndex = componentIndexes

        self.__check_list(rays)
        self.__pool = list(rays.copy())
        self.__rays_num = len(rays) // self.__ComIndex.RAY_OFFSET

        # normalisation of direction vector
        for i in range(self.__rays_num):
            self.normalise_e(i)

    def normalise_e(self, index: int):
        norm_val = np.linalg.norm(self.e(index))
        if abs(norm_val - 1) > np.finfo(float).eps:
            r_i = index * self.__ComIndex.RAY_OFFSET
            for i in range(r_i, r_i + self.__ComIndex.DIM):
                self.__pool[i] /= norm_val

    def append_rays(self, rays: list):
        self.__check_list(rays)
        # extends list, appending at end of list all element from current list
        self.__pool.extend(rays)

        old_size = self.__rays_num
        self.refresh___rays_num()
        for num_ray in range(old_size, self.__rays_num):
            self.normalise_e(num_ray)

    def refresh___rays_num(self):
        val = len(self.__pool) / self.__ComIndex.RAY_OFFSET
        if not isinstance(val, int):
            raise ValueError("ray number is not instance of integer(%s)".format(str(val.__class__.__name__)))
        self.__rays_num = val

    def erase_ray(self, index: int):
        RaysPool.__check_index(self, index)

        from_index = index * self.__ComIndex.RAY_OFFSET
        # part of ray will shift to the left
        until_index = (self.__rays_num - 1) * self.__ComIndex.RAY_OFFSET
        # shift on the deleting ray
        for i in range(from_index, until_index):
            self.__pool[i] = self.__pool[i + self.__ComIndex.RAY_OFFSET]
        # delete last ray
        for i in range(self.__ComIndex.RAY_OFFSET):
            # delete element at the end of list or on index - list.pop(index)
            self.__pool.pop()
        RaysPool.refresh___rays_num(self)

    # ================================================Magic methods=================================================

    def __str__(self):
        s = 'rays pool:\n'

        for i in range(self.__rays_num):
            s += ('%-2s- %s: %-42s, %s: %-44s, %s: %-18s, %s: %-18s, %s: %-18s\n'
                  % (str(i),
                     str(self.__ComIndex.E_OFFSET), str(self.e(i)),
                     str(self.__ComIndex.R_OFFSET), str(self.r(i)),
                     str(self.__ComIndex.T0_OFFSET), str(self.t0(i)),
                     str(self.__ComIndex.T1_OFFSET), str(self.t1(i)),
                     str(self.__ComIndex.l_OFFSET), str(self.l(i)))
                  )
        return s

    def __len__(self):
        return self.__rays_num

    # ================================================Getters=================================================

    def get(self, i: int, needed_offset: (type(Compon2D.RAY_OFFSET), type(Compon3D.RAY_OFFSET))):
        """
        Not recomended to use
        :param i: index of ray
        :param needed_offset:
        :return:
        """
        r_i = i * self.__ComIndex.RAY_OFFSET
        next_offset = None
        for i in self.__ComIndex:
            if i > needed_offset:
                next_offset = i
        return self.__pool[r_i + needed_offset:r_i + next_offset]

    def e(self, i: int) -> list:
        r_i = i * self.__ComIndex.RAY_OFFSET
        a = r_i + self.__ComIndex.E_OFFSET
        b = r_i + self.__ComIndex.R_OFFSET
        return self.__pool[a:b]

    def r(self, i: int):
        r_i = i * self.__ComIndex.RAY_OFFSET
        a = r_i + self.__ComIndex.R_OFFSET
        b = r_i + self.__ComIndex.T0_OFFSET
        return self.__pool[a:b]

    def t0(self, i: int) -> float:
        r_i = i * self.__ComIndex.RAY_OFFSET
        return self.__pool[r_i + self.__ComIndex.T0_OFFSET]

    def t1(self, i) -> float:
        r_i = i * self.__ComIndex.RAY_OFFSET
        return self.__pool[r_i + self.__ComIndex.T1_OFFSET]

    def l(self, i) -> float:
        r_i = i * self.__ComIndex.RAY_OFFSET
        return self.__pool[r_i + self.__ComIndex.l_OFFSET]

    @property
    def componentIndexes(self):
        return self.__ComIndex

    # ================================================Setters=================================================
    # calculate from radius vector of ray
    def set_t0(self, i: int, t0: float):
        if t0 < 0:
            raise AttributeError("Negative length(%f)" % (t0))
        r_i = i * self.__ComIndex.RAY_OFFSET
        self.__pool[r_i + self.__ComIndex.T0_OFFSET] = t0

    # calculate from radius vector of ray
    def set_t1(self, i: int, t1: float):
        if t1 < 0:
            raise AttributeError("Negative length(%f)" % (t1))
        if t1 < self.t0(i):
            raise AttributeError("Length less than begin of ray t0(%f), t1(%f)" % (self.t0(i), t1))
        r_i = i * self.__ComIndex.RAY_OFFSET
        self.__pool[r_i + self.__ComIndex.T1_OFFSET] = t1

    # calculate from radius vector of ray
    def set_l(self, i: int, l: float):
        if l < 0:
            raise AttributeError("Negative optical path(%f)" % (l))
        r_i = i * self.__ComIndex.RAY_OFFSET
        self.__pool[r_i + self.__ComIndex.l_OFFSET] = l

    # methods of object RaysPool========================================================================================
    @staticmethod
    def __reflect_refract(func):
        # обертываем функцию
        def f(self, surface: Surface, push_non_reflected_ray: bool = False):
            rays = []
            # для заполения ячеек, куда мы не можем положить информацию (вычитаем два вектора e и r и начало и конец луча)
            remain_len = self.__ComIndex.RAY_OFFSET - (2 * self.__ComIndex.DIM + 2)
            empty_list = [None for i in range(remain_len)]
            # моделируем отражние
            for i in range(len(self)):
                r, e, t1 = func(self.e(i), self.r(i), surface)
                if len(e) == 0 or len(r) == 0 or t1 is None:
                    if push_non_reflected_ray:
                        from_index = i * self.__ComIndex.RAY_OFFSET
                        to_index = from_index + self.__ComIndex.RAY_OFFSET
                        rays.extend(self.__pool[from_index:to_index])
                    else:
                        continue
                else:
                    self.set_t1(i, t1)
                    rays.extend(e)
                    rays.extend(r)
                    rays.append(0)
                    rays.append(-1)
                    rays.extend(empty_list)
            if len(rays) == 0:
                return None
            return RaysPool(rays, self.__ComIndex)

        return f

    def reflect(self, surface: Surface, push_non_reflected_ray: bool = False):
        ray_pool_reflect = RaysPool.__reflect_refract(ARay.reflect_)
        return ray_pool_reflect(self, surface, push_non_reflected_ray)

    def refract(self, surface: Surface, push_non_refracted_ray: bool = False):
        ray_pool_reflect = RaysPool.__reflect_refract(ARay.refract_)
        return ray_pool_reflect(self, surface, push_non_refracted_ray)

    def calc_point_of_ray(self, i: int, t: float) -> list:
        return ARay.calc_point_of_ray_(self.e(i), self.r(i), t)

    def r1(self, h: float) -> list:
        """
        :param h: length of rays
        :return: list of points for length h:
        """
        return [self.calc_point_of_ray_(self.e(i), self.r(i), h)
                for i in range(self.__rays_num)]
