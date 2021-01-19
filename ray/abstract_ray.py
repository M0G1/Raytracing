import numpy as np
import math as m
from typing import List

from surfaces.surface import Surface

# static methods of ray====================================================================
from abc import ABCMeta, abstractmethod, abstractproperty


class ARay():
    """
        Abstract ray class with few static methods
    """

    @abstractmethod
    def refract(self, surface: Surface):
        "Refract from surface"

    @abstractmethod
    def reflect(self, surface: Surface):
        "Refract from surface"

    @staticmethod
    def calc_point_of_ray_(e: (list, iter), r: (list, iter), t: float) -> list:
        return list(np.add(np.multiply(t, e), r))

    @staticmethod
    def find_norm_vec_and_point(e: (list, np.ndarray), r: (list, np.ndarray), surface: Surface):
        # Шаг-1 ищем точку пересечения
        t = surface._ray_surface_intersection(e, r)
        if len(t) == 0:
            return [], [], None
        point = ARay.calc_point_of_ray_(e, r, t[0])
        # ШАГ-2 ищем вектор нормали к поверхности
        nrm = surface.norm_vec(point)
        if nrm is None or abs(np.dot(nrm, e)) < np.finfo(float).eps * 2:
            return [], [], None
        return point, nrm, t

    @staticmethod
    def refract_(e: (list, np.ndarray), r: (list, np.ndarray), surface: Surface):
        point, nrm, t = ARay.find_norm_vec_and_point(e, r, surface)
        if len(point) == 0 and len(nrm) == 0 and t is None:
            return [], [], None
        # ШАГ-3 преломляем луч
        n1, n2 = surface.get_refractive_indexes(ARay.calc_point_of_ray_(e, r, t[0] / 2))
        # calc the formula of refraction
        v1 = np.dot(n1, e)
        v1n = np.dot(v1, nrm)
        expression = 1 + (n2 ** 2 - n1 ** 2) / (v1n ** 2)
        if expression < 0:
            return ARay.full_internal_reflection(e, nrm, point, t)
        k = (m.sqrt(expression) - 1) * v1n
        e = np.dot(1 / n2, v1 + np.dot(k, nrm))
        return list(point), list(e), t[0]

    # def reflect_(e: (List[float or int], np.ndarray), r: list, surface: Surface):
    @staticmethod
    def reflect_(e: (list, np.ndarray), r: (list, np.ndarray), surface: Surface):
        point, nrm, t = ARay.find_norm_vec_and_point(e, r, surface)
        if len(point) == 0 and len(nrm) == 0 and t is None:
            return [], [], None
        # ШАГ-3 отражаем луч
        e_n = 2 * np.dot(e, nrm)
        e = np.subtract(e, np.dot(e_n, nrm))
        e = np.dot(1 / np.linalg.norm(e), e)
        return list(point), list(e), t[0]

    @staticmethod
    def full_internal_reflection(e: (list, np.ndarray), nrm: (list, np.ndarray), point: (list, np.ndarray), t):
        e_n = 2 * np.dot(e, nrm)
        e = np.subtract(e, np.dot(e_n, nrm))
        e = np.dot(1 / np.linalg.norm(e), e)
        return list(point), list(e), t[0]
