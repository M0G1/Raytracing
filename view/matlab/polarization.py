"""
    Drawing methods for polarisation
    Methods of working with polarisation look at controllers.polarisation.py
"""
import numpy as np
import pylab

from tools import numpy_tool
from tools.generators import Generator
from controllers.polarization import get_param_ellipse_polar, get_str_view_polar_vec
from view.matlab import general


def get_ellipse_points_from_alpha_beta(alpha: float, beta: float, return_point_count: int = 100, is_need_check=True):
    """
        alpha - polarization ellipse azimuth.   -pi/2 <= alpha <= pi/2
        beta - angle of ellipticity.            -pi/4 <= beta <= pi/4
        return_point_count - count of return points om ome axis. Must be more than 3
    """
    if is_need_check:
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
    if beta > 0:
        fi = np.linspace(0, 2 * np.pi, return_point_count)
    else:
        fi = np.linspace(2 * np.pi, 0, return_point_count)
    x = a * np.cos(fi)
    y = b * np.sin(fi)

    if abs(alpha) > np.finfo(np.float_).eps:
        xy = numpy_tool.reshape_arrays_into_one(x, y)
        xy = np.reshape(xy, (xy.size // 2, 2))
        rot_mat = Generator.get_rot_mat_2d(alpha)
        xy = np.matmul(xy, rot_mat)
        xy = xy.ravel()
        x, y = numpy_tool.reshape_array_into_many(xy, row_count=2, column_count=return_point_count)
    return x, y




def draw_arrow_to_polarization(x: (np.array, list, tuple), y: (np.array, list, tuple),
                               xlim: (np.array, list, tuple), ylim: (np.array, list, tuple),
                               beta: float, count_of_arrow_on_ellipse: int = 2):
    if len(xlim) != len(ylim) != 2:
        raise ValueError(f"Limits must have length equals xlim {xlim}, ylim {ylim}")
    xy = (xlim[0], ylim[0], xlim[1], ylim[1])
    arrow_width = np.linalg.norm(np.subtract(xy[:2], xy[2:])) * 0.005

    if abs(beta) > np.finfo(float).eps:
        d_b_a = len(x) // count_of_arrow_on_ellipse
        for i in range(1, count_of_arrow_on_ellipse + 1):
            dba_i_minus_1 = d_b_a * i - 1
            dx = 0
            dy = 0
            if i != count_of_arrow_on_ellipse:
                dx = x[d_b_a * i] - x[dba_i_minus_1]
                dy = y[d_b_a * i] - y[dba_i_minus_1]
                pylab.arrow(x[dba_i_minus_1], y[dba_i_minus_1], dx, dy,
                            length_includes_head=True, width=arrow_width)
            else:
                dx = x[len(x) - 1] - x[len(x) - 2]
                dy = y[len(x) - 1] - y[len(x) - 2]
                pylab.arrow(x[len(x) - 2], y[len(x) - 2], dx, dy, length_includes_head=True, width=arrow_width)
    else:
        # min/max with index search
        indexes = [0, 0]
        x_val = [x[0], x[0]]
        for i in range(1, len(x)):
            if x[indexes[0]] > x[i]:
                x_val[0] = x[i]
                indexes[0] = i
            if x[indexes[1]] < x[i]:
                x_val[1] = x[i]
                indexes[1] = i
        y_val = [y[indexes[0]], y[indexes[1]]]
        for i in range(2):
            dx = 0
            dy = 0
            if indexes[i] + 1 >= len(x):
                dx = x_val[i] - x[indexes[i] - 1]
                dy = y_val[i] - y[indexes[i] - 1]
                x_val[i] = x[indexes[i] - 1]
                y_val[i] = y[indexes[i] - 1]
            else:
                dx = x[indexes[i] + 1] - x_val[i]
                dy = y[indexes[i] + 1] - y_val[i]

            pylab.arrow(x_val[i], y_val[i], dx, dy, length_includes_head=True, width=arrow_width)


def draw_polar_ellipse(vec: (np.array, list, tuple), count_drawing_point: int = 100, count_of_arrow_on_ellipse: int = 2,
                       fp: int = 2, title: str = "", float_dtype=np.float64, **kwargs):
    """
        Drawing polarization for given Jonson vector.
        vec - Jonson vector is two dimensional vector with complex numbers
        count_drawing_point - count of drawing point. Not recommended to use value less than 10.
        fp - float precision
        title - title of figure
        float_dtype - numpy type of float data ()


    """
    if not (float_dtype in (np.float32, np.float64, np.complex64, np.complex128)):
        float_dtype = np.float64
    alpha_, beta = get_param_ellipse_polar(vec, float_dtype=float_dtype)
    x, y = get_ellipse_points_from_alpha_beta(alpha_, beta, is_need_check=False, return_point_count=count_drawing_point)
    color = kwargs.setdefault("color", "blue")

    xlim, ylim = general.focus_on_without_cutting((-1, 1), (-1, 1), x, y, 0.1)
    pylab.xlim(*xlim)
    pylab.ylim(*ylim)
    labelstr = (f"alpha = %.{fp}f,beta = %.{fp}f)") % (alpha_, beta)
    pylab.plot(x, y, color=color, label=labelstr)
    if not title:
        formatstr = get_str_view_polar_vec(vec, fp, float_dtype=float_dtype)
        pylab.title(formatstr)
    else:
        pylab.title(title)
    pylab.legend()
    draw_arrow_to_polarization(x, y, xlim, ylim, beta, count_of_arrow_on_ellipse)
