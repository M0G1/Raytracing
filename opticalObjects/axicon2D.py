"""Module used for research the axicon and Frenel coefficients"""

import numpy as np
import pylab

from surfaces.surface import Surface
from surfaces.plane import Plane
from surfaces.limited_surface import LimitedSurface
from ray.ray import Ray

import controllers.modeling_controller as modelCtrl


def create_axicon(angle: float, is_isosceles: bool, lenght_of_side_ribs: float, is_closed: bool,
                  refr_coef_inside: float, refr_coef_outside: float):
    """
    :param angle: the angle betweet OX and side rib (degree from 0 to 90)
    :param is_isosceles: if true, then the triangle is isosceles. Else rectangular.
    :param lenght_of_side_ribs: more than 0
    :param is_closed: if true, then list surfaces have 3 objects. Else 2.
    :return: list of the limited surfaces. Two vertex of axicon is on OX. One at point (0,0)
    """
    if not (refr_coef_inside >= 1 and refr_coef_outside >= 1):
        return None
    if not (angle > 0 and angle < 90):
        return None
    if not (lenght_of_side_ribs > 0):
        return None

    refr_coef = [refr_coef_inside, refr_coef_outside]
    length = lenght_of_side_ribs
    angle = angle * np.pi / 180
    sinA = np.sin(angle)
    cosA = -np.cos(angle)
    dir_vec = [cosA, sinA]
    x, y = [val * length for val in dir_vec]
    m = [[0, -1],
         [1, 0]]
    norm = list(np.dot(dir_vec, m))
    line1 = Plane([0, 0], norm, Surface.types.REFRACTING, n1=refr_coef[0], n2=refr_coef[1])
    line2 = None
    if is_isosceles:
        norm2 = norm.copy()
        norm2[1] *= -1
        line2 = Plane([0, 0], norm2, Surface.types.REFRACTING, n1=refr_coef[0], n2=refr_coef[1])
    else:
        line2 = Plane([0, 0], [0, -1], Surface.types.REFRACTING, n1=refr_coef[0], n2=refr_coef[1])
    limits1 = [[x, 0],
               [0, y]]
    limits2 = [[x, 0],
               [-y, 0]]
    line1 = LimitedSurface(line1, limits1)
    line2 = LimitedSurface(line2, limits2)
    if is_closed:
        line3 = Plane([x, 0], [-1, 0], Surface.types.REFRACTING, n1=refr_coef[0], n2=refr_coef[1])
        limits3 = [[x - np.finfo(float).eps, x + np.finfo(float).eps],
                   [-y, y]]
        if not is_isosceles:
            limits3[1] = [0, y]
        line3 = LimitedSurface(line3, limits3)
        return (line1, line2, line3)
    return (line1, line2)


def draw_axicon2D(surfaces: list, axes, is_isosceles: bool = True):
    """
    draw axicon
    :param surfaces: surfaces from method create_axicon()
    :param axes: pylab.gca()
    :param is_isosceles:
    :return:
    """
    if not all([isinstance(i, LimitedSurface) for i in surfaces]):
        return False
    xy = [surfaces[0].limits[0][0], surfaces[0].limits[1][1]]

    l1 = pylab.Line2D([xy[0], 0], [xy[1], 0])
    l2 = None
    l3 = None
    if is_isosceles:
        l2 = pylab.Line2D([xy[0], 0], [-xy[1], 0])
        l3 = pylab.Line2D([xy[0], xy[0]], [xy[1], -xy[1]])
    else:
        l3 = pylab.Line2D([xy[0], xy[0]], [xy[1], 0])
        l2 = pylab.Line2D([xy[0], 0], [0, 0])
    axes.add_line(l3)
    axes.add_line(l2)
    axes.add_line(l1)


def get_points_of_func_frenel_from_refr_coef(
        type_polarization: str,
        ray: Ray, ray_index: int,
        axicon: list, deep,
        refr_axicon_coef: list, step: float):
    """

    :param type_polarization: p or s
    :param ray:ray_index:
    :param ray_index: ray after what will be calculate Frenel coefficients. You must know it!
    :param axicon: from method create_axicon()
    :param deep: deep modeling. depth of tree of ray
    :param refr_axicon_coef: list from 2 values (n1,n2) n2 >n1
    :param step: step of discreditation
    :return:
    Take a graph of the dependence of the Fresnel coefficients on the refractive index for rays coming after a given.
    (x coordinates, y coordinates)
    """
    if len(refr_axicon_coef) != 2 or not (refr_axicon_coef[1] > refr_axicon_coef[0]):
        raise AttributeError("Incorrect refract coefficients %s" % (str(refr_axicon_coef)))

    cur_n = refr_axicon_coef[0]
    end_n = refr_axicon_coef[1]
    x_coor = []
    refl_coef = [x_coor, []]
    transmittance = [x_coor, []]

    refraction_indexs = axicon[0].get_refractive_indexes([1, 1])
    refraction_outside_index = refraction_indexs[0]

    while end_n >= cur_n:  # np.finfo(float).eps:
        for i in axicon:
            i.set_refractive_indexes(cur_n, refraction_outside_index)

        # log
        print("n: ", cur_n)
        for i in axicon:
            print(i)

        tree = modelCtrl.deep_modeling(type_polarization, ray, axicon, deep)
        subtree = None

        for i, sub_tree in enumerate(tree):
            if i == ray_index:
                subtree = sub_tree
                break

        fall_ray = subtree.value
        reflect_ray = None
        refract_ray = None
        R = None
        T = None

        if subtree.left is not None:
            reflect_ray = subtree.left.value
            R = reflect_ray.bright / fall_ray.bright
        if subtree.right is not None:
            refract_ray = subtree.right.value
            T = refract_ray.bright / fall_ray.bright
        if T is None and R is not None:
            T = 0
            R = 1
        if R is None and T is not None:
            R = 0
            T = 1

        # log
        print("fall ray: ", fall_ray)
        print("reflect ray: ", reflect_ray)
        print("R: ", R)
        print("refract ray: ", refract_ray)
        print("T: ", T, '\n')

        x_coor.append(cur_n)
        refl_coef[1].append(R)
        transmittance[1].append(T)

        cur_n = cur_n + step

    print("x_coor", x_coor)
    print("refl_coef", refl_coef[1])
    print("transmittance", transmittance[1])

    for i in axicon:
        i.set_refractive_indexes(refraction_indexs[0], refraction_outside_index)

    return (refl_coef, transmittance)
