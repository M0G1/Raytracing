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


def get_points_of_func_frenel(
        type_polarization: str,
        ray: Ray, ray_indexes: (list, tuple),
        axicon: list,
        refr_axicon_coef: list, step: float):
    """

       :param type_polarization: p or s
       :param ray:ray_index:
       :param ray_indexes: rays after what will be calculate Frenel coefficients. You must know it!
       :param axicon: from method create_axicon()
       :param refr_axicon_coef: list from 2 values (n1,n2) n2 >n1
       :param step: step of discreditation
       :return:
       Take a graph of the dependence of the Fresnel coefficients on the refractive index for rays coming after a given.
       refration_indexes, refl_coef, transmittance
       refl_coef, transmittance is a list, where every element is calculated coefficients for every ray in ray_indexes
       """
    if len(refr_axicon_coef) != 2 or not (refr_axicon_coef[1] > refr_axicon_coef[0]):
        raise AttributeError("Incorrect refract coefficients %s" % (str(refr_axicon_coef)))

    # save using the memory
    deep = np.max(ray_indexes) + 1
    cur_n = refr_axicon_coef[0]
    end_n = refr_axicon_coef[1]
    x_coor = []
    refl_coef = [[] for i in range(len(ray_indexes))]
    transmittance = [[] for i in range(len(ray_indexes))]

    refraction_indexs = axicon[0].get_refractive_indexes([1, 1])
    refraction_outside_index = refraction_indexs[0]

    check = []

    while end_n >= cur_n:  # np.finfo(float).eps:
        # set next refractive index in the axicon
        for i in axicon:
            i.set_refractive_indexes(cur_n, refraction_outside_index)

        # trace ray
        tree = modelCtrl.deep_modeling(type_polarization, ray, axicon, deep)
        subtree_list = list()

        # search needed ray in tree
        for i, sub_tree in enumerate(tree):
            if i in ray_indexes:
                subtree_list.append(sub_tree)
                # print(f"{i} - {sub_tree.value}")
                # print(f"left {sub_tree.left.value}")
                # print(f"right {sub_tree.right.value}\n")

        # check.append(subtree_list)
        # calculate frenel indexes
        for i, subtree in enumerate(subtree_list):
            # calculate frenel indexes for current ray
            fall_ray = subtree.value
            reflect_ray = subtree.left.value if subtree.left is not None else None
            refract_ray = subtree.right.value if subtree.right is not None else None
            R, T = get_frenel_coef(fall_ray, reflect_ray, refract_ray)

            # save the data in list
            refl_coef[i].append(R)
            transmittance[i].append(T)
        # add the refraction index
        x_coor.append(cur_n)
        # next refractive index
        cur_n = cur_n + step

    # print(f"x_coor:\n{x_coor}")
    # print(f"refl_coef: len = {len(refl_coef)},len of first el = {len(refl_coef[0])}\n{np.asarray(refl_coef)}")
    # print(
    #     f"transmittance: len = {len(transmittance)},len of first el = {len(transmittance[0])}\n{np.asarray(transmittance)}")

    # check_str = ""
    # for s in check:
    #     check_str += (str(s) + "\n")
    # # print(f"\n check=\n{ check_str}")
    return x_coor, refl_coef, transmittance


def get_points_of_func_frenel_from_refr_coef(
        type_polarization: str,
        ray: Ray, ray_index: int,
        axicon: list,
        refr_axicon_coef: list, step: float):
    """
    :param type_polarization: p or s
    :param ray:ray_index:
    :param ray_index: ray after what will be calculate Frenel coefficients. You must know it!
    :param axicon: from method create_axicon()
    :param refr_axicon_coef: list from 2 values (n1,n2) n2 >n1
    :param step: step of discreditation
    :return:
    Take a graph of the dependence of the Fresnel coefficients on the refractive index for rays coming after a given.
    refl_coef, transmittance is a list of calculated coefficients
    """
    if len(refr_axicon_coef) != 2 or not (refr_axicon_coef[1] > refr_axicon_coef[0]):
        raise AttributeError("Incorrect refract coefficients %s" % (str(refr_axicon_coef)))

    cur_n = refr_axicon_coef[0]
    end_n = refr_axicon_coef[1]
    x_coor = []
    refl_coef = []
    transmittance = []

    refraction_indexs = axicon[0].get_refractive_indexes([1, 1])
    refraction_outside_index = refraction_indexs[0]

    while end_n >= cur_n:  # np.finfo(float).eps:
        # set next refractive index in the axicon
        for i in axicon:
            i.set_refractive_indexes(cur_n, refraction_outside_index)

        # log
        print("n: ", cur_n)
        for i in axicon:
            print(i)

        # trace ray
        # deep =  ray_index + 1, because it save the memory
        tree = modelCtrl.deep_modeling(type_polarization, ray, axicon, ray_index + 1)
        subtree = None

        # search needed ray in tree
        for i, sub_tree in enumerate(tree):
            if i == ray_index:
                subtree = sub_tree
                break

        # calculate frenel indexes
        fall_ray = subtree.value
        reflect_ray = subtree.left.value if subtree.left is not None else None
        refract_ray = subtree.right.value if subtree.right is not None else None
        R, T = get_frenel_coef(fall_ray, reflect_ray, refract_ray)

        # log
        print("fall ray: ", fall_ray)
        print("reflect ray: ", reflect_ray)
        print("R: ", R)
        print("refract ray: ", refract_ray)
        print("T: ", T, '\n')

        # save the data in list
        x_coor.append(cur_n)
        refl_coef.append(R)
        transmittance.append(T)
        # next refractive index
        cur_n = cur_n + step

    print("x_coor", x_coor)
    print("refl_coef", refl_coef)
    print("transmittance", transmittance)

    # return old refraction index
    for i in axicon:
        i.set_refractive_indexes(refraction_indexs[0], refraction_outside_index)

    return x_coor, refl_coef, transmittance


def get_frenel_coef(fall_ray: Ray, reflect_ray: Ray, refract_ray: Ray):
    R = None
    T = None
    if reflect_ray is not None:
        R = reflect_ray.bright #/ fall_ray.bright
    if refract_ray is not None:
        T = refract_ray.bright #/ fall_ray.bright
    if T is None and R is not None:
        T = 0
        R = 1
    if R is None and T is not None:
        R = 0
        T = 1

    return R, T
