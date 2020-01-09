import numpy as np
import math as m

from surfaces.surface import Surface


# static methods of ray====================================================================

def calc_point_of_ray_(e: list, r: list, t: float) -> list:
    return list(np.add(np.multiply(t, e), r))


"""
"""


def find_norm_vec_and_point(e: list, r: list, surface: Surface):
    # Шаг-1 ищем точку пересечения
    t = surface._ray_surface_intersection(e, r)
    if len(t) == 0:
        return [], [], None
    point = calc_point_of_ray_(e, r, t[0])
    # ШАГ-2 ищем вектор нормали к поверхности
    nrm = surface.norm_vec(point)
    if nrm is None:
        return [], [], None
    return point, nrm, t


def refract(e: list, r: list, surface: Surface):
    point, nrm, t = find_norm_vec_and_point(e, r, surface)
    if len(point) == 0 and len(nrm) == 0 and t is None:
        return [], [], None
    # ШАГ-3 преломляем луч
    n1, n2 = surface.get_refractive_indexes(r)
    # calc the formula of refraction
    v1 = np.dot(n1, e)
    v1n = np.dot(v1, nrm)
    expression = 1 + (n2 ** 2 - n1 ** 2) / (v1n ** 2)
    if expression < 0:
        return reflect(e, r, surface)
    k = (m.sqrt(expression) - 1) * v1n
    e = np.dot(1 / n2, v1 + np.dot(k, nrm))
    return list(point), list(e), t[0]


def reflect(e: list, r: list, surface: Surface):
    point, nrm, t = find_norm_vec_and_point(e, r, surface)
    if len(point) == 0 and len(nrm) == 0 and t is None:
        return [], [], None
    # ШАГ-3 отражаем луч
    e_n = 2 * np.dot(e, nrm)
    e = np.subtract(e, np.dot(e_n, nrm))
    e = np.dot(1 / np.linalg.norm(e), e)
    return list(point), list(e), t[0]
