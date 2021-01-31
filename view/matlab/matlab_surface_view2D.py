import numpy as np
import pylab
import matplotlib.patches as patches

from ray.abstract_ray import ARay
import view.matlab.sphere_ellipse_data2D as spell

from surfaces.surface import Surface
from surfaces.plane import Plane
from surfaces.sphere import Sphere
from surfaces.ellipse import Ellipse
from surfaces.limited_surface import LimitedSurface


def draw_plane(plane: Plane, color="blue", alpha=0.5):
    # matrix of rotation
    m = [[0, -1],
         [1, 0]]
    # direction vector
    r = np.dot(m, plane.norm_vec([]))
    # coords = vray.collect_point_to_draw(r,)
    point = [ARay.calc_point_of_ray_(r, plane.rad, 10_000),
             ARay.calc_point_of_ray_(r, plane.rad, -10_000)]

    line = pylab.Line2D([point[i][0] for i in range(2)],
                        [point[i][1] for i in range(2)], color=color, alpha=alpha)
    pylab.gca().add_line(line)


def draw_sphere(sphere: Sphere, color='b', alpha=0.5):
    sphere = pylab.Circle(sphere.center, sphere.r, fill=False, color=color, alpha=alpha)
    pylab.gca().add_patch(sphere)


def draw_ellipse(ellipse: Ellipse, color='b', alpha=0.5):
    ellipse = patches.Ellipse(ellipse.center, 2 * ellipse.abc[0], 2 * ellipse.abc[1], fill=False, color='b', alpha=0.5)
    pylab.gca().add_patch(ellipse)


def draw_limited_plane(plane: LimitedSurface, color="blue", alpha=0.5):
    surface = plane.surface
    if not isinstance(surface, Plane):
        return
    norm = surface.norm_vec(point=[])
    const = np.dot(surface.rad, norm)
    limits = plane.limits
    # keep the unique values
    x = {-(const + limits[1][i] * norm[1]) / norm[0] for i in range(2)}
    y = {-(const + limits[0][i] * norm[0]) / norm[1] for i in range(2)}
    x.update(limits[0])
    y.update(limits[1])

    x = list(x)
    y = list(y)

    line = None
    belong_points = set()
    for k in range(len(x)):
        for l in range(len(y)):
            point = (x[k], y[l])
            if surface.is_point_belong(point) and plane._is_point_in_limits(point):
                belong_points.add(point)

    belong_points = list(belong_points)
    if len(belong_points) == 2:
        line = pylab.Line2D([belong_points[i][0] for i in range(2)],
                            [belong_points[i][1] for i in range(2)])
        pylab.gca().add_line(line)
    return


def draw_limited_ellipse(ellipse: LimitedSurface, color='b', alpha=0.5):
    # получаем коэфициенты растяжения по осям
    to_draw = None

    # получаем коэфициенты растяжения по осям
    surface = ellipse.surface
    lim = ellipse.limits

    if isinstance(surface, Sphere):
        center = surface.center
        to_draw = spell.Sphere_Ellipse_data_2Dview.get_sphere2D(10 ** -2, center, surface.r)
    elif isinstance(surface, Ellipse):
        center = surface.center
        to_draw = spell.Sphere_Ellipse_data_2Dview.get_ellipse2D(10 ** -2, center, surface.abc)
    else:
        return

        # quenes
    to_cuting_pre = [to_draw]
    to_cuing_cur = []

    for k in range(len(lim)):
        while len(to_cuting_pre) > 0:
            val = to_cuting_pre.pop(0)
            to_cuing_cur.extend(__cut(val, lim, k))

        to_cuting_pre = to_cuing_cur
        to_cuing_cur = []

    for line in to_cuting_pre:
        pylab.plot(line[0], line[1], color=color, alpha=alpha)


def __cut(to_draw: iter, lim: iter, k: int) -> iter:

    # делаем срезы по одной осям
    xy_index_begin = []
    xy_index_end = []
    in_range_prev = False
    i = 0
    for i, val in enumerate(to_draw[k]):
        exp = lim[k][0] <= val and val <= lim[k][1]
        if exp != in_range_prev:
            if exp:
                xy_index_begin.append(i)
            else:
                xy_index_end.append(i)
        in_range_prev = exp

    if len(xy_index_end) < len(xy_index_begin):
        xy_index_end.append(len(to_draw[0]))

    to_draw2 = []
    for i, j in zip(xy_index_begin, xy_index_end):
        to_draw2.append([])
        to_draw2[len(to_draw2) - 1].append(to_draw[0][i:j])
        to_draw2[len(to_draw2) - 1].append(to_draw[1][i:j])
    return to_draw2


def draw_limits(surface: LimitedSurface, color: str = "black", alpha: float = 0.5):
    lim = surface.limits
    planes = [
        Plane([lim[0][0], 0], [1, 0]),
        Plane([lim[0][1], 0], [1, 0]),
        Plane([0, lim[1][0]], [0, 1]),
        Plane([0, lim[1][1]], [0, 1]),
    ]
    for plane in planes:
        draw_plane(plane, color=color, alpha=alpha)


def draw_exist_surface(surface: Surface, color: str = "blue", alpha: float = 1.):
    """
        draw existing surface: Plane,Sphere,Ellipse and
        LimitedSurface, where surface is limited Plane,Sphere,Ellipse
    :return:
    """
    if isinstance(surface, Plane):
        draw_plane(surface, color=color, alpha=alpha)
    elif isinstance(surface, Sphere):
        draw_sphere(surface, color=color, alpha=alpha)
    elif isinstance(surface, Ellipse):
        draw_ellipse(surface, color=color, alpha=alpha)
    elif isinstance(surface, LimitedSurface):
        inner_surface = surface.surface
        if isinstance(inner_surface, Plane):
            draw_limited_plane(surface, color=color, alpha=alpha)
        elif isinstance(inner_surface, (Sphere, Ellipse)):
            draw_limited_ellipse(surface, color=color, alpha=alpha)
    else:
        raise AttributeError("Not supporting surface " + str(surface))
