import numpy as np
from typing import List, Union

from ray.abstract_ray import ARay
from surfaces.surface import Surface
from ray.additional.component_struct import *

LOWER_BOUND_OF_T0_RAY_BEGIN = 10 ** -15


class RaysPool(ARay):
    """
        Class of list of rays. Each ray has its index in the array.
        It have access methods: e,r,t0,t1 etc. (see more in methods)
        And some data manipulating ones: reflect,refract.
        Also it have a few list method "appends_rays" "erase_ray".

        This class contains rays. A ray is described by an enumeration (see file "ray.additional.component_struct.py")
         which contains the offsets from the origin (as for 1 ray) for the ray parameter.
        For Example, direction of rays is n-dimension vector of real number.
        It designation E_OFFSET. starting from index E_OFFSET, the direction data is located in separate
        cells of the list.
    """

    @staticmethod
    def __check_type(lst):
        if not all(isinstance(i, (float, int, complex)) or (i is None) for i in lst):
            raise TypeError("vector of direction and radius vector must consist from float or integer number")

    @staticmethod
    def __check_comIndex(compon_index_class):
        if not issubclass(compon_index_class, ComponInterface):
            raise AttributeError("compon_index_class must be the class Compon2D or Compon3D." +
                                 " And you take %s" % str(compon_index_class))

    def __check_index(self, index: int):
        if index < 0 or index >= self.__rays_num:
            raise IndexError("Incorrect index(%s)" % (str(index)))

    def __check_list(self, lst: list):
        if (len(lst) % self.__ComIndex.RAY_OFFSET) != 0:
            raise AttributeError("Invalid length of rays list(%d). It must be multiplied  by %d" % (
                len(lst), self.__ComIndex.RAY_OFFSET))
        RaysPool.__check_type(lst)

    # ================================================Object's=================================================

    def __init__(self, rays: (list, iter), compon_index_class, default_ray_length: float = 1):
        """
        :param rays: iterable object with Numeric values. It is lenght must be a multiple value of RAY_OFFSET
         of class Compon2D or Compon3D
        :param compon_index_class: class Compon2D or Compon3D with needed dimension space
        """

        self.__check_comIndex(compon_index_class)
        self.__ComIndex = compon_index_class
        self.default_ray_length = default_ray_length

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

    def refresh_rays_num(self):
        val = len(self.__pool) / self.__ComIndex.RAY_OFFSET
        if not isinstance(val, int):
            raise ValueError("ray number is not instance of integer(%s)".format(str(val.__class__.__name__)))
        self.__rays_num = val

    def append_rays(self, rays: list):
        self.__check_list(rays)
        # extends list, appending at end of list all element from current list
        self.__pool.extend(rays)

        old_size = self.__rays_num
        self.refresh_rays_num()
        for num_ray in range(old_size, self.__rays_num):
            self.normalise_e(num_ray)

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
        RaysPool.refresh_rays_num(self)

    # ================================================Magic methods=================================================

    def __str__(self):
        s = 'rays pool:\n'

        for i in range(self.__rays_num):
            s += ('%-2s- %s: %-44s, %s: %-44s, %s: %-20s, %s: %-20s, %s: %-18s\n'
                  % (str(i),
                     str(self.__ComIndex.E_OFFSET), str(self.e(i)),
                     str(self.__ComIndex.R_OFFSET), str(self.r(i)),
                     str(self.__ComIndex.T0_OFFSET), str(self.t0(i)),
                     str(self.__ComIndex.T1_OFFSET), str(self.t1(i)),
                     str(self.__ComIndex.L_OFFSET), str(self.l(i)))
                  )
        return s

    def __len__(self):
        return self.__rays_num

    # ================================================ Getters =========================================================
    def get(self, needed_offset: (Compon2D, Compon3D, ComponInterface), i: int):
        """
        :param i: index of ray
        :param needed_offset: value of
        :return: value for i-th ray of given value offset. If it have a few values, return a vector of values
        Example
        direction offset is E_OFFSET in classes Compon2D Compon3D
        if u call "get(0, Compon2D.E_OFFSET)" it return the two dimensional vector of real numbers
        if u call "get(0, Compon3D.T0_OFFSET)" it return the real numbers
        """
        r_i = i * self.__ComIndex.RAY_OFFSET
        next_offset = get_next_offset(self.__ComIndex, needed_offset)
        if next_offset - needed_offset > 1:
            return self.__pool[r_i + needed_offset:r_i + next_offset]
        else:
            return self.__pool[r_i + needed_offset]

    def e(self, i: int) -> Union[List[float or int], np.ndarray]:
        return self.get(self.__ComIndex.E_OFFSET, i)

    def r(self, i: int) -> Union[List[float or int], np.ndarray]:
        return self.get(self.__ComIndex.R_OFFSET, i)

    def t0(self, i: int) -> Union[float or int]:
        return self.get(self.__ComIndex.T0_OFFSET, i)

    def t1(self, i) -> Union[float or int]:
        return self.get(self.__ComIndex.T1_OFFSET, i)

    def l(self, i) -> Union[float or int]:
        return self.get(self.__ComIndex.L_OFFSET, i)

    def jones_vec(self, i) -> Union[List[complex or float or int], np.ndarray]:
        return self.get(self.__ComIndex.Jo_OFFSET, i)

    @property
    def compon_index_class(self):
        return self.__ComIndex

    def begin_ray(self, i: int) -> np.ndarray:
        """Return the point(numpy.array) of begin of ray"""
        return np.add(self.r(i), np.dot(self.t0(i), self.e(i)))

    def end_ray(self, i: int) -> np.ndarray:
        """Return the point(numpy.array) of end of ray"""
        t1 = self.default_ray_length
        if self.t1(i) > 0:
            t1 = self.t1(i)
        return np.add(self.r(i), np.dot(t1, self.e(i)))

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
            raise ValueError("Negative optical path(%f)" % l)
        r_i = i * self.__ComIndex.RAY_OFFSET
        self.__pool[r_i + self.__ComIndex.L_OFFSET] = l

    def set_jones_vec(self, i: int, jo_vec: Union[List[complex or float or int], np.ndarray]):
        r_i = i * self.__ComIndex.RAY_OFFSET
        beg = r_i + self.__ComIndex.Jo_OFFSET
        end = r_i + get_next_offset(self.__ComIndex, self.__ComIndex.Jo_OFFSET)
        self.__pool[beg:end] = jo_vec

    # =============================================== Vector operation =================================================

    def get_vector(self, needed_offset: (Compon2D, Compon3D, ComponInterface), begin: int = 0, end: int = -1):
        """
        eturns a vector of values for the passed offset value.
        In this case, the indices of those rays are taken that are in the half-interval [begin,end)

        :param needed_offset  Some parameter, what u want get.
        :param begin  index of start, after(this include) what will collect data. Default = 0
        :param end  index of finish, before(this doesn't include) what will collect data. Default = -1 (mean all rays)
        """
        end = end if end != -1 else len(self) - 1
        data = []
        next_offset = get_next_offset(self.__ComIndex, needed_offset)
        if next_offset - needed_offset > 1:
            for i in range(begin, end):
                r_i = i * self.__ComIndex.RAY_OFFSET
                data.append(self.__pool[r_i + needed_offset:r_i + next_offset])
        else:
            for i in range(begin, end):
                r_i = i * self.__ComIndex.RAY_OFFSET
                data.append(self.__pool[r_i + needed_offset])
        return data

    def get_points_for_lengths(self, t: (List[float or int], np.ndarray), begin: int = 0, end: int = -1):
        """
        eturn coordinates of ray for given lengths "t"
        :param t  the values of ray length. The size of "t" must equal "end - begin".
        :param begin  index of start, after(this include) what will collect data. Default = 0
        :param end  index of finish, before(this doesn't include) what will collect data. Default = -1 (mean all rays)
        """
        if len(t) != (end - begin):
            raise ValueError(f"Size of list t must equal 'end - begin'({end - begin}). But it have size {len(t)}")
        r = self.get_vector(self.__ComIndex.R_OFFSET, begin, end)
        e = np.asarray(self.get_vector(self.__ComIndex.E_OFFSET, begin, end))
        return np.add(r, np.multiply(t, e.T).T)

    def get_points_for_length(self, h: (float, int), begin: int = 0, end: int = -1) -> list:
        """
        eturn coordinates of ray for given length "t"
        :param t - the value of ray length.
        :param begin - index of start, after(this include) what will collect data. Default = 0
        :param end - index of finish, before(this doesn't include) what will collect data. Default = -1 (mean all rays)
        """
        end = end if end != -1 else len(self) - 1
        vec_size = end - begin
        return self.get_points_for_lengths(np.full((vec_size,), h), begin, end)

    def begin_ray_vector(self, begin: int = 0, end: int = -1):
        """
        :param return coordinates of ray start
        :param begin - index of start, after(this include) what will collect data. Default = 0
        :param end - index of finish, before(this doesn't include) what will collect data. Default = -1 (mean all rays)
        """
        t0 = self.get_vector(self.__ComIndex.T0_OFFSET, begin, end)
        return self.get_points_for_lengths(t0, begin, end)

    def end_ray_vector(self, begin: int = 0, end: int = -1):
        """
        Return coordinates of ray start
        :param begin - index of start, after(this include) what will collect data. Default = 0
        :param end - index of finish, before(this doesn't include) what will collect data. Default = -1 (mean all rays)
        """
        t1 = self.get_vector(self.__ComIndex.T1_OFFSET, begin, end)
        cond = t1 < 0
        t1[cond] = self.default_ray_length
        return self.get_points_for_lengths(t1, begin, end)

    # methods of object RaysPool========================================================================================
    @staticmethod
    def __reflect_refract(func):
        # обертываем функцию
        def f(self, surface: Surface, push_non_reflected_ray: bool = False):
            rays = []
            # для заполения ячеек, куда мы не можем положить информацию
            # (вычитаем длины двух векторов e и r и начало и конец луча)
            remain_len = self.__ComIndex.RAY_OFFSET - (2 * self.__ComIndex.DIM + 2)
            empty_list = [None] * remain_len
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
                    rays.append(LOWER_BOUND_OF_T0_RAY_BEGIN)
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
