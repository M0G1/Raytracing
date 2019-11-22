import pylab
import numpy as np

from ray.ray import Ray
from utility.binarytree import Tree

def draw_deep_ray_modeling(tree: Tree, axes, color='r'):
    count_of_rays = len(tree)
    for i, subtree in enumerate(tree):
        if isinstance(subtree.value, Ray):
            val = subtree.value
            # ,linewidth=count_of_rays - i
            line = pylab.Line2D(val._Ray__path_of_ray[0], val._Ray__path_of_ray[1], color=color,
                                alpha=(count_of_rays - i) / count_of_rays)
            x_dir_of_text = [1, 0]
            y_dir_of_text = [0, 1]
            # для определения направления надписи относительно уже известного
            dir_of_ray = [coordinate[1] - coordinate[0] for coordinate in val._Ray__path_of_ray]
            dir_of_ray_norm = np.linalg.norm(dir_of_ray)
            x_scalar_mul = np.dot(x_dir_of_text, dir_of_ray) / dir_of_ray_norm
            y_scalar_mul = np.dot(y_dir_of_text, dir_of_ray) / dir_of_ray_norm
            x_angle_of_rotation = int((np.arccos(x_scalar_mul) * 360 / 2 * np.pi))
            y_angle_of_rotation = int((np.arccos(y_scalar_mul) * 360 / 2 * np.pi))
            angle_of_rotation = None
            if y_angle_of_rotation <= 90:
                angle_of_rotation = x_angle_of_rotation
            else:
                angle_of_rotation = 360 - x_angle_of_rotation

            point_label = [np.average(coor) for coor in val._Ray__path_of_ray]
            x_point_label = np.average(val._Ray__path_of_ray[0])
            y_point_label = np.average(val._Ray__path_of_ray[1])
            m = [[0, 1],
                 [-1, 0]]
            norm_dir_of_ray = np.linalg.norm(dir_of_ray)
            norm_to_ray = np.dot(np.dot(dir_of_ray, m), 1 / norm_dir_of_ray)

            point_label = np.add(point_label, norm_to_ray * 0.05)
            axes.text(point_label[0], point_label[1], str(i + 1), va='center')

            line.set_label(str(i + 1))
            axes.add_line(line)