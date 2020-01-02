import numpy as np
import math as m

from surfaces.surface import Surface


# static methods of ray====================================================================

def calc_point_of_ray_(e: list, r: list, t: float) -> list:
    return list(np.add(np.multiply(t, e), r))


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


def is_total_returnal_refraction(ray, surface: Surface) -> bool:
    # list, list, float
    point, nrm, t_1 = find_norm_vec_and_point(ray.dir, ray.start, surface)
    if len(point) == 0 and len(nrm) == 0 and t_1 is None:
        return False
    ray.t1 = t_1[0]
    # ШАГ-3 преломляем луч
    n1, n2 = surface.get_refractive_indexes(ray.start)
    # calc the formula of refraction
    v1 = np.dot(n1, ray.dir)
    v1n = np.dot(v1, nrm)
    expression = 1 + (n2 ** 2 - n1 ** 2) / (v1n ** 2)
    return expression < 0


def get_angle_between_rays(ray1, ray2) -> float:
    return np.arccos(np.dot(ray1.dir, ray2.dir))


def calc_s_polar_frenel_coef(fall_ray_amplitude: float, alpha: float, beta: float, nu1: float = 1, nu2: float = 1):
    if fall_ray_amplitude <= 0:
        raise AttributeError("Amplitude less or equal zero " + str(fall_ray_amplitude))
    # if nu1 == nu2 == 1:
    #     s_amp = fall_ray_amplitude * (2 * np.sin(alpha) * np.cos(beta)) / np.sin(alpha + beta)
    #     q_amp =
    #     return (s_amp)
    expression = (nu1 * np.tan(alpha)) / (nu2 * np.tan(beta))
    s_amp = 2 / (1 + expression)
    q_amp = (1 - expression) / (1 + expression)

    s_amp *= fall_ray_amplitude
    q_amp *= fall_ray_amplitude
    return (s_amp, q_amp)


def calc_s_polar_frenel_coef(fall_ray_amplitude: float, alpha: float, beta: float):
    if fall_ray_amplitude <= 0:
        raise AttributeError("Amplitude less or equal zero " + str(fall_ray_amplitude))
    sin_a_b = np.sin(alpha + beta)
    s_amp = 2 * np.cos(alpha) * np.sin(beta) / sin_a_b
    q_amp = np.sin(beta - alpha) / sin_a_b

    s_amp *= fall_ray_amplitude
    q_amp *= fall_ray_amplitude
    return (s_amp, q_amp)


def calc_s_polar_frenel_coef(fall_ray_amplitude: float, alpha: float, beta: float, n1: float, n2: float):
    if fall_ray_amplitude <= 0:
        raise AttributeError("Amplitude less or equal zero " + str(fall_ray_amplitude))
    if n1 < 1 or n2 < 1:
        raise AttributeError("Refractive indices less than unity. n1: {}, n2: {}".format(n1, n2))
    n1_cos_a = n1 * np.cos(alpha)
    n2_cos_b = n2 * np.cos(beta)
    expression = n1_cos_a + n2_cos_b

    s_amp = 2 * n1_cos_a / expression
    q_amp = (n1_cos_a - n2_cos_b) / expression

    s_amp *= fall_ray_amplitude
    q_amp *= fall_ray_amplitude
    return (s_amp, q_amp)


def calc_p_polar_frenel_coef(fall_ray_amplitude: float, alpha: float, beta: float, nu1: float = 1, nu2: float = 1,
                             eps1: float = 1, eps2: float = 1):
    if fall_ray_amplitude <= 0:
        raise AttributeError("Amplitude less or equal zero " + str(fall_ray_amplitude))
    sin_2a = np.sin(2 * alpha)
    sin_2b = np.sin(2 * beta)
    nu1_nu2 = nu1 / nu2
    nu1_n2_sin_2a = nu1_nu2 * sin_2a
    sqrt = 2 * np.sqrt(nu1_nu2 * eps1 / eps2)

    s_amp = sqrt * sin_2a / (nu1_n2_sin_2a + sin_2b)
    q_amp = (nu1_n2_sin_2a - sin_2b) / (nu1_n2_sin_2a + sin_2b)

    s_amp *= fall_ray_amplitude
    q_amp *= fall_ray_amplitude
    return (s_amp, q_amp)


def calc_p_polar_frenel_coef(fall_ray_amplitude: float, alpha: float, beta: float):
    if fall_ray_amplitude <= 0:
        raise AttributeError("Amplitude less or equal zero " + str(fall_ray_amplitude))
    a_b = alpha - beta
    a_p_b = alpha + beta
    s_amp = 2 * np.cos(alpha) * np.sin(beta) / (np.sin(a_p_b) * np.cos(a_b))
    q_amp = np.tan(a_b) / np.tan(a_p_b)

    s_amp *= fall_ray_amplitude
    q_amp *= fall_ray_amplitude
    return (s_amp, q_amp)


def calc_frenel_coef(type_polarisation: str, fall_ray_amplitude: float, alpha: float, beta: float,
                     nu1: float = 1,
                     nu2: float = 1,
                     eps1: float = 1, eps2: float = 1, n1: float = 1, n2: float = 1):
    if type_polarisation[0] == 's':
        if nu1 == 1 and nu2 == 1:
            if n1 == 1 and n2 == 1:
                return calc_s_polar_frenel_coef(fall_ray_amplitude, alpha, beta)
            return calc_s_polar_frenel_coef(fall_ray_amplitude, alpha, beta, n1=n1, n2=n2)
        return calc_s_polar_frenel_coef(fall_ray_amplitude, alpha, beta, nu1=nu1, nu2=nu2)
    elif type_polarisation[0] == 'p':
        if nu1 == 1 and nu2 == 1 and eps1 == 1 and eps2 == 1:
            return calc_p_polar_frenel_coef(fall_ray_amplitude, alpha, beta)
        return calc_p_polar_frenel_coef(fall_ray_amplitude, alpha, beta, nu1, nu2, eps1, eps2)
    return None
