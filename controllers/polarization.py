"""
    This module include the tools with working polarisation.
    Jones calculus here is used.
    Jones vector is a two dimensional vector with complex numbers.
            /E_DX\   /A_X * e^(i * fi_X) \
    E_D =   \E_DY/ = \A_Y * e^(i * fi_Y)/
    module |E_D| = A = sqrt(A_X **2 + A_Y **2)
    normal Jones vector
            /e_X\   /a_X*e^(i*fi_X) \
    E_D =   \e_Y/ = \a_Y*e^(i*fi_Y)/

    e - ellipticity
    e = b/a = tg(beta)

    alpha - polarization ellipse azimuth.   -pi/2 <= alpha <= pi/2
    beta - angle of ellipticity.            -pi/4 <= beta <= pi/4

    sing of beta show direction of polarization.
    For positive beta - right polarisation.
    For negative - left polarisation.

    Еhe vector electric field strength rotates clockwise for an observer
    looking in the opposite direction of radiation propagation,
    then the polarization is called right elliptical, else left.
"""
import numpy as np
import pylab

from tools import help
from tools.generators import Generator


def is_2d_complex_vector(vec: (np.array, list, tuple)):
    if len(vec) != 2:
        return False
    if any([not isinstance(vec[i], (float, int, complex)) for i in range(2)]):
        return False
    return True


def get_param_ellipse_polar(vec: (np.array, list, tuple), is_need_check=True):
    """
        vec - Jones vector(two dimensional vector with complex numbers)
        Return (alpha,Beta)

        alpha - polarization ellipse azimuth.   -pi/2 <= alpha <= pi/2
        beta - angle of ellipticity.            -pi/4 <= beta <= pi/4

        sing of beta show direction of polarization.
        For positive beta - right polarisation.
        For negative - left polarisation.

        Еhe vector electric field strength rotates clockwise for an observer
        looking in the opposite direction of radiation propagation,
        then the polarization is called right elliptical, else left.
    """
    if is_need_check:
        if not is_2d_complex_vector(vec):
            raise ValueError(f"Argument vec {vec} is not Jones vector")
    xi: complex = complex(0, 0)
    if abs(vec[0]) > np.finfo(np.float_).eps:
        xi: complex = vec[1] / vec[0]
    alpha = np.arctan(2 * xi.real / (1 - np.absolute(xi) ** 2)) / 2
    beta = np.arcsin(2 * xi.imag / (1 + np.absolute(xi) ** 2)) / 2
    return (alpha, beta)


def get_ellipse_points_from_alpha_beta(alpha: float, beta: float, return_point_count: int = 100, is_need_check=True):
    """
        alpha - polarization ellipse azimuth.   -pi/2 <= alpha <= pi/2
        beta - angle of ellipticity.            -pi/4 <= beta <= pi/4
        return_point_count - count of return points om ome axis. Must be more than 3
    """
    if is_need_check:
        if abs(beta) < np.finfo(float).eps:
            raise ValueError(f"Beta is too close to zero or equal zero b={beta}")
        if not (-np.pi / 2 <= alpha <= np.pi / 2) or \
                not (-np.pi / 4 <= beta <= np.pi / 4):
            raise ValueError(f"-pi/2 <= alpha <= pi/2, -pi/4 <= beta <= pi/4. Given val alpha = {alpha}, beta = {beta}")
        if return_point_count <= 1:
            raise ValueError(f"return_point_count is less than 4 ({return_point_count}).")
    a = abs(np.cos(beta))
    b = abs(np.sin(beta))

    # СДЕЛАТЬ МЕТОД У ПОВЕРХНОСТЕЙ ВОЗВРАЩАЮЩИЙ МАССИВЫ С ТОЧКАМИ ДЛЯ ОТОБРАЖЕНИЯ
    # СДЕЛАТЬ ВРАЩАЮЩУЮСЯ ПОВЕРХНОСТЬ
    # и возвращать вращнный эллипс
    fi = None
    if beta < 0:
        fi = np.linspace(0, 2 * np.pi, return_point_count)
    else:
        fi = np.linspace(-2 * np.pi, 0, return_point_count)
    x = a * np.cos(fi)
    y = b * np.sin(fi)

    if abs(alpha) > np.finfo(np.float_).eps:
        xy = help.reshape_arrays_into_one(x, y)
        xy = np.reshape(xy, (xy.size // 2, 2))
        rot_mat = Generator.get_rot_mat_2d(alpha)
        xy = np.matmul(xy, rot_mat)
        xy = xy.ravel()
        x, y = help.reshape_array_into_many(xy, row_count=2, column_count=return_point_count)
    return x, y


def draw_polar_ellipse(vec: (np.array, list, tuple)):
    alpha_, beta = get_param_ellipse_polar(vec)
    x, y = get_ellipse_points_from_alpha_beta(alpha_, beta, is_need_check=False)
    COUNT_OF_ARROW_ON_ELLIPSE = 5
    d_b_a = len(x) // COUNT_OF_ARROW_ON_ELLIPSE  # distance between arrow on ellipse in count of point
    for i in range(1, COUNT_OF_ARROW_ON_ELLIPSE):
        dba_i_minus_1 = d_b_a * i - 1
        pylab.plot(x[d_b_a * (i - 1):dba_i_minus_1], y[d_b_a * (i - 1):dba_i_minus_1])
        dx = x[d_b_a * i] - x[dba_i_minus_1]
        dy = y[d_b_a * i] - y[dba_i_minus_1]
        pylab.arrow(x[dba_i_minus_1], y[dba_i_minus_1], dx, dy)
