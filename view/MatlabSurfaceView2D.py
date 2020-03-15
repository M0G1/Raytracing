import numpy as np
import pylab
import matplotlib.patches as patches
import math
import queue

from ray.abstract_ray import ARay
from ray.ray import Ray
import ray.rays_pool as rays_pool
import view.MatlabRayView2D as vray
import view.sphereEllipseReadWrite as spell

from utility.binarytree import Tree

from surfaces.surface import Surface
from surfaces.plane import Plane
from surfaces.sphere import Sphere
from surfaces.ellipse import Ellipse
from surfaces.limited_surface import LimitedSurface


def draw_plane(plane: Plane, color="blue", alpha=0.5) -> bool:
    # matrix of rotation
    m = [[0, -1],
         [1, 0]]
    # direction vector
    r = np.dot(m, plane._Plane__norm)
    # coords = vray.collect_point_to_draw(r,)
    point = [ARay.calc_point_of_ray_(r, plane.rad, 10_000),
             ARay.calc_point_of_ray_(r, plane.rad, -10_000)]
    print("dro", [point[i][0] for i in range(2)])

    line = pylab.Line2D([point[i][0] for i in range(2)],
                        [point[i][1] for i in range(2)], color=color, alpha=alpha)
    pylab.gca().add_line(line)
    return True


def draw_sphere(sphere: Sphere, axes: type(pylab.gca()), color='b', alpha=0.5) -> bool:
    sphere = pylab.Circle(sphere.center, sphere.r, fill=False, color=color, alpha=alpha)
    axes.add_patch(sphere)
    del sphere
    return True


def draw_ellipse(ellipse: Ellipse, axes: type(pylab.gca()), color='b', alpha=0.5):
    ellipse = patches.Ellipse(ellipse.center, 2 * ellipse.abc[0], 2 * ellipse.abc[1], fill=False, color='b', alpha=0.5)
    axes.add_patch(ellipse)
    del ellipse
    return True


def draw_limited_plane(plane: LimitedSurface, axes: type(pylab.gca()), color="blue", alpha=0.5) -> bool:
    line = pylab.Line2D(plane.limits[0], plane.limits[1])
    axes.add_line(line)
    return True


def draw_limited_ellipse(ellipse: LimitedSurface, color='b', alpha=0.5):
    # получаем коэфициенты растяжения по осям
    to_draw = None

    # получаем коэфициенты растяжения по осям
    surface = ellipse.surface
    lim = ellipse.limits
    center = surface.center
    if isinstance(surface, Sphere):
        to_draw = spell.Sphere_Ellipse_data_2Dview.get_sphere2D(10 ** -2, center, surface.r)
    elif isinstance(surface, Ellipse):
        to_draw = spell.Sphere_Ellipse_data_2Dview.get_ellipse2D(10 ** -2, center, surface.abc)

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
