import pylab
import numpy as np

from ray.ray import Ray
import ray.rays_pool as rays_pool
from utility.binarytree import Tree
import controllers.raySurfaceController as rsc


def draw_ray(axes, way_points_of_ray: list, color="green"):
    if len(way_points_of_ray) == 2:
        axes.add_line(pylab.Line2D(way_points_of_ray[0], way_points_of_ray[1], color=color, marker=''))
    if len(way_points_of_ray) == 3:
        axes.plot(
            way_points_of_ray[0],
            way_points_of_ray[1],
            way_points_of_ray[2],
            label='LINE', color=color);
        axes.scatter(way_points_of_ray[0],
                     way_points_of_ray[1],
                     way_points_of_ray[2],
                     c='b', marker='o')


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
            # x_scalar_mul = np.dot(x_dir_of_text, dir_of_ray) / dir_of_ray_norm
            # y_scalar_mul = np.dot(y_dir_of_text, dir_of_ray) / dir_of_ray_norm
            # x_angle_of_rotation = int((np.arccos(x_scalar_mul) * 360 / 2 * np.pi))
            # y_angle_of_rotation = int((np.arccos(y_scalar_mul) * 360 / 2 * np.pi))
            # angle_of_rotation = None
            # if y_angle_of_rotation <= 90:
            #     angle_of_rotation = x_angle_of_rotation
            # else:
            #     angle_of_rotation = 360 - x_angle_of_rotation

            # x_point_label = np.average(val._Ray__path_of_ray[0])
            # y_point_label = np.average(val._Ray__path_of_ray[1])

            point_label = [np.average(coor) for coor in val._Ray__path_of_ray]
            m = [[0, 1],
                 [-1, 0]]
            norm_dir_of_ray = np.linalg.norm(dir_of_ray)
            norm_to_ray = np.dot(np.dot(dir_of_ray, m), 1 / norm_dir_of_ray)
            point_label = np.add(point_label, norm_to_ray * norm_dir_of_ray / 50)
            print("norm_dir_of_ray", norm_dir_of_ray)
            axes.text(point_label[0], point_label[1], str(i + 1), va='center', size=8)

            line.set_label(str(i + 1))
            axes.add_line(line)
            print('dir of ray', dir_of_ray)
            print('line', line)
            print('val._Ray__path_of_ray', val._Ray__path_of_ray)
            print('line ', i + 1, ' drawed')
            print()


def draw_ray_pool(pool: rays_pool.RaysPool):
    if rays_pool.Compon.DIM.value != 2:
        raise AttributeError("NON-two-dimensional ray pool")
    for i in range(len(pool)):
        x_coor = []
        y_coor = []

        begin = rsc.calc_point_of_ray_(pool.e(i), pool.r(i), pool.t0(i))
        t1 = 1
        if pool.t1(i) is not None:
            t1 = pool.t1(i)
        end = rsc.calc_point_of_ray_(pool.e(i), pool.r(i), t1)

        x_coor.append([begin[0], end[0]])
        y_coor.append([begin[1], end[1]])

        line = pylab.Line2D(x_coor, y_coor)
        axes = pylab.gca()
        axes.add_line(line)


if __name__ == '__main__':
    print(np.sqrt(-1), " ", isinstance(np.sqrt(-1), (float, int)))
    size = 5.5
    pylab.xlim(-size, size)
    pylab.ylim(-size, size)
    pylab.gca().add_line(pylab.Line2D([1, 2], [1, 2]))
    pylab.show()