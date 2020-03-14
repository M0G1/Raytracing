import numpy as np
import pylab
import matplotlib.patches as patches
import math

from ray.abstract_ray import ARay
from ray.ray import Ray
import ray.rays_pool as rays_pool

from utility.binarytree import Tree

from surfaces.surface import Surface
from surfaces.plane import Plane
from surfaces.sphere import Sphere
from surfaces.ellipse import Ellipse
from surfaces.limited_surface import LimitedSurface


def draw_plane(plane: Plane, axes: type(pylab.gca()), color="blue", alpha=0.5) -> bool:
    # matrix of rotation
    m = [[0, -1],
         [1, 0]]
    # direction vector
    r = np.dot(m, plane.__norm)

    point = [ARay.calc_point_of_ray_(plane.rad, r, 10_000),
             ARay.calc_point_of_ray_(plane.rad, r, -10_000)]
    line = pylab.Line2D([point[i][0] for i in range(2)],
                        [point[i][1] for i in range(2)], color=color, alpha=alpha)
    axes.add_line(line)
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


def draw_limited_ellipse(ellipse: LimitedSurface, axes: type(pylab.gca()), color='b', alpha=0.5):
    # получаем коэфициенты растяжения по осям
    ab = []
    if isinstance(ellipse.surface, Sphere):
        ab = [ellipse.surface.r, ellipse.surface.r]
    elif isinstance(ellipse.surface, Ellipse):
        ab = ellipse.surface.abc

    # получаем коэфициенты растяжения по осям
    lim = ellipse.limits
    center = ellipse.surface.center

    print("1", (lim[1][0] - center[1]) / ab[1])
    print("2", (lim[1][1] - center[1]) / ab[1])
    print("3", (lim[0][0] - center[0]) / ab[0])
    print("4", (lim[0][1] - center[0]) / ab[0])
    print("center", center)
    # находим пересечения по оси Абсцис(Х)
    expression = [(ab[0] ** 2) * (1 - ((lim[1][i] - center[1]) / ab[1]) ** 2) for i in range(2)]
    x_check = [var >= 0 for var in expression]

    print("exp", expression, "\n")

    x0 = None
    x1 = None

    if x_check[0]:
        x0 = math.sqrt(expression[0]) + center[0]
    if x_check[1]:
        x1 = math.sqrt(expression[1]) + center[0]

    # находим пересечения по оси Ординат(Y)
    expression = [(ab[1] ** 2) * (1 - ((lim[0][i] - center[0]) / ab[0]) ** 2) for i in range(2)]
    y_check = [var >= 0 for var in expression]

    print("exp", expression, "\n")

    y0 = None
    y1 = None

    if y_check[0]:
        y0 = np.sqrt(expression[0]) + center[1]
    if y_check[1]:
        y1 = np.sqrt(expression[1]) + center[1]

    # удаляем ненужные уже поля
    del x_check
    del y_check
    del expression
    del center
    del lim

    print()
    print("x0", x0)
    print("x1", x1)
    print("y0", y0)
    print("y1", y1)
    print()

    # находим значения углов
    if x0 is not None:
        angle = math.acos(x0)
        x0 = (-angle, angle)
    else:
        x0 = (-math.pi, math.pi)
    if x1 is not None:
        angle = math.acos(x1)
        x1 = [angle, -angle + 2 * math.pi]
    else:
        x1 = (0, 2 * math.pi)

    if y0 is not None:
        angle = math.asin(y0)
        y0 = (angle, - angle + 2 * math.pi)
    else:
        y0 = (0, 2 * math.pi)
    if y1 is not None:
        angle = math.asin(y1)
        y1 = (-math.pi - angle, angle)
    else:
        y1 = (-math.pi, math.pi)

    # фиксируем одну и добираемё
    # x0 x0[0] < x0[1] (0, 0) (-pi, pi)
    # x1 x1[0] < x1[1] (0, 2pi) (pi, pi)

    # y0 y0[0] < y0[1] (0, 2pi) (pi, pi)
    # y1 y1[0] < y1[1] (-pi, pi) (-2pi, 0)
    x = [x0, x1]
    y = [y0, y1]
    intersect = [__ss(a, b, __return_intersection) for a in x for b in y]
    inter = []
    for j in intersect:
        if not (j is None):
            for i in j:
                if i is not None:
                    inter.append(i)

    print("\ninter 1", inter)

    intersect = []
    for i, a in enumerate(inter):
        for j in range(i + 1, len(inter)):
            res = __ss(a, inter[j], __unite_)
            if res[0]:
                intersect.append(res[1])
            else:
                intersect.append(res[1][0])
    inter = []

    print("union 2", intersect)

    for i in range(len(intersect) - 1):
        inter.append(__shift_nearest(intersect[i], intersect[i + 1])[0])
    inter.append(intersect[len(intersect) - 1])

    print("shift 3", inter, "\n")

    # сделать отрисовку этого безобразия
    for i in inter:
        r = np.arange(start=i[0], stop=i[1], step=0.01)
        x = ab[0] * np.cos(r)
        y = ab[1] * np.sin(r)
        line = pylab.Line2D(x, y, color=color, alpha=alpha)
        axes.add_line(line)
    return True


def __return_intersection(a: iter, b: iter):
    if abs(a[0] - a[1]) < 10 * np.finfo(float).eps:
        return None
    if abs(b[0] - b[1]) < 10 * np.finfo(float).eps:
        return None

    left = None
    right = None
    if a[1] > b[0] or b[1] < a[0]:
        return None

    if a[0] > b[0]:
        left = b[0]
    else:
        left = a[0]

    if a[1] > b[1]:
        right = b[1]
    else:
        right = a[1]

    return (left, right)


def __unite_(a: iter, b: iter):
    if abs(a[0] - a[1]) < 10 * np.finfo(float).eps:
        return None
    if abs(b[0] - b[1]) < 10 * np.finfo(float).eps:
        return None

    if a[1] > b[0] and a[1] < b[1]:
        return (True, (a[0], b[1]))
    if b[1] > a[0] and b[1] < a[1]:
        return (True, (b[0], a[1]))
    return (False, (a, b))


def __ss(a: iter, b: iter, func):
    if abs(a[0] - a[1]) < 10 * np.finfo(float).eps:
        return None
    if abs(b[0] - b[1]) < 10 * np.finfo(float).eps:
        return None
    shifts = ((0, 0), (2 * math.pi, 2 * math.pi), (-2 * math.pi, -2 * math.pi))
    for i in range(3):
        br = False
        for j in range(3):
            i1 = func(np.add(a, shifts[i]), np.add(b, shifts[j]))
            if i1 != None:
                br = True
                break
        if br:
            break


def __shift_nearest(a: iter, b: iter):
    shifts = ((0, 0), (2 * math.pi, 2 * math.pi), (-2 * math.pi, -2 * math.pi))
    k = 0
    l = 0
    min = 1000
    for i in range(3):
        for j in range(3):
            i1 = np.min(np.abs(np.subtract(np.add(a, shifts[i]), np.add(b, shifts[j]))))
            if i1 < min:
                k = i
                l = j
                min = i1
    return (np.add(a, shifts[k]), np.add(a, shifts[l]))
