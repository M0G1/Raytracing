import numpy as np
import pylab

from surfaces.surface import Surface
from ray.ray import Ray
from utility.binarytree import Tree
import controllers.rayController as rc
import controllers.rayStaticController as rsCTRL


def _not_sequence_modeling(ray: Ray, surfaces: list):
    min_p = float(np.finfo(float).max)
    # index of nearest surface and intersection point
    index, i_point = -1, None
    for i in range(len(surfaces)):
        point = surfaces[i].find_nearest_point_intersection(ray)
        if point is None or len(point) == 0:
            continue
        norm_val = np.linalg.norm(np.subtract(ray.start, point))
        if norm_val < min_p:
            min_p = norm_val
            index = i
            i_point = point
    return index, i_point


def deep_modeling(type_polarization:str,ray: Ray, surfaces: list, deep: int) ->Tree:
    if not all(isinstance(some, Surface) for some in surfaces):
        raise AttributeError(
            "Not all elements in surfaces is instance of class Surface %s" % (
                str([type(some) for some in surfaces]))
        )
    if deep < 1:
        raise AttributeError(
            "Invalid deep value(%s)" % (
                str(deep))
        )

    if type_polarization != 's' and type_polarization != 'p':
        raise AttributeError(
            "Enter correct value of type polarization (s or p). You enter: %s" % (
                type_polarization)
        )

    def fill_ray_tree(tree: Tree, surfaces: list, deep: int):
        ray_ = tree.value

        # index of nearest surface and intersection point
        index, i_point = _not_sequence_modeling(ray_, surfaces)
        reflect_ray = None
        refract_ray = None
        exit = False

        if i_point == None:
            tree.left = None
            tree.right = None
            exit = True
            i_point = ray_.calc_point_of_ray(1)

        _append_point_to_path(ray_, ray_._Ray__path_of_ray, i_point)
        if deep < 0:
            return

        if exit:
            return

        if rc.is_total_returnal_refraction(ray_, surfaces[index]):
            reflect_ray = Ray.reflect(ray_, surfaces[index])
            tree.left = Tree(reflect_ray)
        else:
            refract_ray = Ray.refract(ray_, surfaces[index])
            tree.right = Tree(refract_ray)
            reflect_ray = Ray.reflect(ray_, surfaces[index])
            tree.left = Tree(reflect_ray)

        point, norm, t = rsCTRL.find_norm_vec_and_point(ray_.dir, ray_.start, surfaces[index])
        n1, n2 = surfaces[index].get_refractive_indexes(ray_.start)
        # , n1, n2
        rc.set_brightness(type_polarization, ray_, refract_ray, reflect_ray, norm,n1,n2)

        if tree.left is not None:
            fill_ray_tree(tree.left, surfaces, deep - 1)
        if tree.right is not None:
            fill_ray_tree(tree.right, surfaces, deep - 1)

    tree = Tree(ray)
    fill_ray_tree(tree, surfaces, deep)
    return tree


def model_path(ray: Ray, surfaces: list, is_return_ray_list: bool = False, is_have_ray_in_infinity: bool = False):
    way_point_of_ray = []
    ray_list = [ray]
    new_ray = ray
    temp = None
    while True:
        min_p = float(np.finfo(float).max)
        # index of nearest surface and intersection point
        # ищем ближайшую поверхность
        index, i_point = -1, None
        index, i_point = _not_sequence_modeling(new_ray, surfaces)
        if i_point == None:
            break
        # print("Surf  " + str(surfaces[index]))
        if surfaces[index].type == Surface.types.REFLECTING:
            temp = new_ray.reflect(surfaces[index])
        elif surfaces[index].type == Surface.types.REFRACTING:
            temp = new_ray.refract(surfaces[index])
        _append_point_to_path(new_ray, way_point_of_ray, temp.start)
        # print(new_ray,temp,'\n')
        if is_return_ray_list:
            ray_list.append(temp)
        new_ray = temp
    if is_have_ray_in_infinity:
        _append_point_to_path(new_ray, way_point_of_ray, rsCTRL.calc_point_of_ray_(new_ray.dir, new_ray.start, 10000))
    if is_return_ray_list:
        return way_point_of_ray, ray_list
    return way_point_of_ray


def _append_point_to_path(ray: Ray, way_points_of_ray: list, point: list):
    # if len(point) == 0:
    #     raise AttributeError("Zero dimensional point")
    # if len(way_points_of_ray) != 0 and (len(point) != len(way_points_of_ray) or ray.dim != len(point)):
    #     raise AttributeError(
    #         """Iterables objects(point) have different length with ray or way_points_of_ray. len(way_points_of_ray):
    #          %d, len(point): %d, ray(%d)""" % (
    #             len(way_points_of_ray), len(point), ray.dim))
    if len(way_points_of_ray) == 0:
        for i in range(ray.dim):
            way_points_of_ray.append([])
        for j in range(ray.dim):
            way_points_of_ray[j].append(ray.start[j])
    for j in range(ray.dim):
        way_points_of_ray[j].append(point[j])


def path_ray_for_drawing(ray: Ray, surfaces: list, is_return_ray_list: bool = False,
                         is_have_ray_in_infinity: bool = False):
    if not all(isinstance(some, Surface) for some in surfaces):
        raise AttributeError(
            "Not all elements in surfaces is instance of class Surface %s" % (
                str([type(some) for some in surfaces]))
        )
    ans = None
    ray_list = None
    if is_return_ray_list:
        ans, ray_list = model_path(ray, surfaces, is_return_ray_list, True)
    else:
        ans = model_path(ray, surfaces, is_have_ray_in_infinity=True)

    if is_return_ray_list:
        return ans, ray_list
    return ans
