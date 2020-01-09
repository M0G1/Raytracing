import numpy as np
import math as m

from surfaces.surface import Surface
from ray.ray import Ray
import controllers.rayStaticController as rsCTRL


def is_total_returnal_refraction(ray: Ray, surface: Surface) -> bool:
    # list, list, float
    point, nrm, t_1 = rsCTRL.find_norm_vec_and_point(ray.dir, ray.start, surface)
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


def get_angle_between_vec(vec1: (list, np.ndarray), vec2: (list, np.ndarray)) -> float:
    cos_val = np.dot(vec1, vec2)
    if (abs(1 - cos_val) <= np.finfo(float).eps * 2):
        return 0
    return np.arccos(cos_val)


"""
:param alpha: falling angle. beta: refract angle
"""


def calc_s_polar_frenel_coef_1(fall_ray_amplitude: float, alpha: float, beta: float, nu1: float = 1, nu2: float = 1):
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


"""
:param alpha: falling angle. beta: refract angle
"""


def calc_s_polar_frenel_coef_2(fall_ray_amplitude: float, alpha: float, beta: float):
    if fall_ray_amplitude <= 0:
        raise AttributeError("Amplitude less or equal zero " + str(fall_ray_amplitude))
    sin_a_b = np.sin(alpha + beta)
    s_amp = 2 * np.cos(alpha) * np.sin(beta) / sin_a_b
    q_amp = np.sin(beta - alpha) / sin_a_b

    s_amp *= fall_ray_amplitude
    q_amp *= fall_ray_amplitude
    return (s_amp, q_amp)


"""
:param alpha: falling angle. beta: refract angle
"""


def calc_s_polar_frenel_coef_3(fall_ray_amplitude: float, alpha: float, beta: float, n1: float, n2: float):
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


"""
:param alpha: falling angle. beta: refract angle
"""


def calc_p_polar_frenel_coef_1(fall_ray_amplitude: float, alpha: float, beta: float, nu1: float = 1, nu2: float = 1,
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


"""
:param alpha: falling angle. beta: refract angle
"""


def calc_p_polar_frenel_coef_2(fall_ray_amplitude: float, alpha: float, beta: float):
    if fall_ray_amplitude <= 0:
        raise AttributeError("Amplitude less or equal zero " + str(fall_ray_amplitude))
    a_b = alpha - beta
    a_p_b = alpha + beta
    s_amp = 2 * np.cos(alpha) * np.sin(beta) / (np.sin(a_p_b) * np.cos(a_b))
    q_amp = np.tan(a_b) / np.tan(a_p_b)

    s_amp *= fall_ray_amplitude
    q_amp *= fall_ray_amplitude
    return (s_amp, q_amp)


"""
:param alpha: falling angle. beta: refract angle
"""


def calc_frenel_coef(type_polarisation: str, fall_ray_amplitude: float, alpha: float, beta: float,
                     nu1: float = 1, nu2: float = 1,
                     eps1: float = 1, eps2: float = 1,
                     n1: float = 1, n2: float = 1):
    if type_polarisation[0] == 's':
        if nu1 == 1 and nu2 == 1:
            if n1 == 1 and n2 == 1:
                return calc_s_polar_frenel_coef_2(fall_ray_amplitude, alpha, beta)
            return calc_s_polar_frenel_coef_3(fall_ray_amplitude, alpha, beta, n1=n1, n2=n2)
        return calc_s_polar_frenel_coef_1(fall_ray_amplitude, alpha, beta, nu1=nu1, nu2=nu2)
    elif type_polarisation[0] == 'p':
        if nu1 == 1 and nu2 == 1 and eps1 == 1 and eps2 == 1:
            return calc_p_polar_frenel_coef_2(fall_ray_amplitude, alpha, beta)
        return calc_p_polar_frenel_coef_1(fall_ray_amplitude, alpha, beta, nu1, nu2, eps1, eps2)
    return None


def set_amplitude(type_polarisation: str, fall_ray: Ray, refract_ray: Ray, reflect_ray: Ray,
                  norm_vec: list):  # , n1: float, n2: float):
    if (fall_ray is None) or (refract_ray is None and reflect_ray is None):
        return
    if (refract_ray is None) and (reflect_ray is not None):
        reflect_ray.A = fall_ray.A
        return
    if (refract_ray is not None) and (reflect_ray is None):
        refract_ray.A = fall_ray.A
        return
    if (norm_vec is None):
        return
    print("norm_vec ", norm_vec)
    a_b = [get_angle_between_vec(reflect_ray.dir, norm_vec),
           get_angle_between_vec(refract_ray.dir, norm_vec)]
    pi_on_2 = np.pi / 2
    for i in range(2):
        if a_b[i] > pi_on_2:
            a_b[i] = np.pi - a_b[i]
    a_b_degree = [180 * i / np.pi for i in a_b]
    # digit calculation have mistakes in angle to close to 90 degree.
    # And is created two rays with different in coordinates  on machine epsilon
    if all(i == 0 for i in a_b_degree):
        refract_ray.A = fall_ray.A - np.finfo(float).eps
        reflect_ray.A = np.finfo(float).eps
        return

    print(fall_ray, reflect_ray, refract_ray, sep='\n')
    print(a_b_degree)

    s_amp, q_amp = calc_frenel_coef(type_polarisation, fall_ray.A, a_b[0], a_b[1])  # , n1=n1, n2=n2)

    reflect_ray.A = q_amp
    refract_ray.A = s_amp


def set_brightness(type_polarisation: str, fall_ray: Ray, refract_ray: Ray, reflect_ray: Ray,
                   norm_vec: list, is_amlitude_calculate: bool = False):
    if (fall_ray is None) or (refract_ray is None and reflect_ray is None):
        return
    if (refract_ray is None) and (reflect_ray is not None):
        reflect_ray.bright = fall_ray.bright
        return
    if (refract_ray is not None) and (reflect_ray is None):
        refract_ray.bright = fall_ray.bright
        return
    if (norm_vec is None):
        return

    reflect_brightness = 1
    refract_brightness = 1
    if is_amlitude_calculate:
        set_amplitude(type_polarisation=type_polarisation,
                      fall_ray=fall_ray, refract_ray=refract_ray, reflect_ray=reflect_ray,
                      norm_vec=norm_vec)

    if is_amlitude_calculate and type_polarisation == "s":
        reflect_brightness = reflect_ray.A ** 2 / fall_ray.A ** 2
        refract_brightness = 1 - reflect_brightness
    else:
        if type_polarisation != 's' and type_polarisation != 'p':
            return
        a_b = [get_angle_between_vec(reflect_ray.dir, norm_vec),
               get_angle_between_vec(refract_ray.dir, norm_vec)]
        pi_on_2 = np.pi / 2
        for i in range(2):
            if a_b[i] > pi_on_2:
                a_b[i] = np.pi - a_b[i]
        # digit calculation have mistakes in angle to close to 90 degree.
        # And is created two rays with different in coordinates  on machine epsilon
        if all(i == 0 for i in a_b):
            refract_ray.bright = fall_ray.bright - np.finfo(float).eps
            reflect_ray.bright = np.finfo(float).eps
            return

        a_plus_b = a_b[0] + a_b[1]
        a_minus_b = a_b[0] - a_b[1]

        sqr_sin_a_p_b = np.sin(a_plus_b) ** 2

        if type_polarisation == 's':
            reflect_brightness = np.sin(a_minus_b) ** 2 / sqr_sin_a_p_b
            refract_brightness = 1 - reflect_brightness
        if type_polarisation == 'p':
            reflect_brightness = np.tan(a_minus_b) ** 2 / np.tan(a_plus_b) ** 2
            refract_brightness = np.sin(2 * a_b[0]) * np.sin(2 * a_b[1]) / (sqr_sin_a_p_b * np.cos(a_minus_b) ** 2)

    reflect_ray.bright = fall_ray.bright * reflect_brightness
    refract_ray.bright = fall_ray.bright * refract_brightness
