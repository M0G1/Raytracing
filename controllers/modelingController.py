import numpy as np

from surfaces.surface import Surface
from ray.ray import Ray
from utility.binarytree import Tree



def _not_sequence_modeling(ray: Ray, surfaces: list):
    min_p = float(np.finfo(float).max)
    # index of nearest surface and intersection point
    index, i_point = -1, None
    for i in range(len(surfaces)):
        point = None
        point = surfaces[i].find_nearest_point_intersection(ray)
        if point == None:
            continue
        norm_val = np.linalg.norm(np.subtract(ray.start, point))
        if norm_val < min_p:
            min_p = norm_val
            index = i
            i_point = point
    return index, i_point


def deep_modeling(ray: Ray, surfaces: list, deep: int):
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

    def fill_ray_tree(tree: Tree, surfaces: list, deep: int):
        ray_ = tree.value

        # index of nearest surface and intersection point
        index, i_point = _not_sequence_modeling(ray_,surfaces)

        exit = False
        if i_point == None:
            tree.left = None
            tree.right = None
            exit = True
            i_point = ray_.calc_point_of_ray(1)

        ray_._Ray__append_point_to_path(ray_._Ray__path_of_ray, i_point)
        if deep < 0:
            return

        if exit:
            return
        if Ray.is_total_returnal_refruction(ray_, surfaces[index]):
            reflect_ray = Ray._reflect(ray_, surfaces[index])
            tree.left = Tree(reflect_ray)
        else:
            refract_ray = Ray._refract(ray_, surfaces[index])
            tree.right = Tree(refract_ray)
            reflect_ray = Ray._reflect(ray_, surfaces[index])
            tree.left = Tree(reflect_ray)
        if tree.left is not None:
            fill_ray_tree(tree.left, surfaces, deep - 1)
        if tree.right is not None:
            fill_ray_tree(tree.right, surfaces, deep - 1)

    tree = Tree(ray)
    fill_ray_tree(tree, surfaces, deep)
    return tree
