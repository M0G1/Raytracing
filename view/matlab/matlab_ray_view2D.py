import pylab
import numpy as np

from ray.ray import Ray
import ray.rays_pool as rays_pool
from utility.binarytree import Tree
from ray.abstract_ray import ARay


def draw_ray(axes, way_points_of_ray: list, color="green"):
    if len(way_points_of_ray) == 2:
        axes.add_line(pylab.Line2D(way_points_of_ray[0], way_points_of_ray[1], color=color, marker=''))
    if len(way_points_of_ray) == 3:
        axes.plot(
            way_points_of_ray[0],
            way_points_of_ray[1],
            way_points_of_ray[2],
            label='LINE', color=color)
        axes.scatter(way_points_of_ray[0],
                     way_points_of_ray[1],
                     way_points_of_ray[2],
                     c='b', marker='o')


def draw_deep_ray_modeling(
        tree: Tree, axes, color='r', lower_limit_brightness: float = 0.01,
        ray_const_length: float = 1, is_real_index: bool = False):
    count_of_rays = len(tree)
    index = 0
    for i, subtree in enumerate(tree):
        if isinstance(subtree.value, Ray):
            index = index + 1
            val = subtree.value

            line = None
            t1 = 1
            isInfiniteRay = False
            if val.t1 != -1:
                t1 = val.t1
            else:
                isInfiniteRay = True
                t1 = ray_const_length

            coords = collect_point_to_draw(val.dir, val.start, 0, t1)
            print("coords", coords)
            bright = None

            if val.bright > lower_limit_brightness:
                bright = val.bright
            else:
                bright = lower_limit_brightness
            line = pylab.Line2D(coords[0], coords[1], color=color, alpha=bright)

            x_dir_of_text = [1, 0]
            y_dir_of_text = [0, 1]
            # для определения направления надписи относительно уже известного
            dir_of_ray = [coordinate[1] - coordinate[0] for coordinate in coords]
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
            point_label = None
            # if isInfiniteRay:
            #     point_label = [0.75, 0.75]
            # else:
            #     pass
            point_label = [np.average(coor) for coor in coords]

            m = [[0, 1],
                 [-1, 0]]
            print("point label ", point_label)
            norm_dir_of_ray = np.linalg.norm(dir_of_ray)
            norm_to_ray = np.dot(np.dot(dir_of_ray, m), 1 / norm_dir_of_ray)
            const = 0.05
            point_label = np.add(point_label, norm_to_ray * const)  # norm_to_ray * norm_dir_of_ray / 50)
            print("norm_dir_of_ray", norm_dir_of_ray)
            if not is_real_index:
                axes.text(point_label[0], point_label[1], str(index), va='center', size=8)
            else:
                axes.text(point_label[0], point_label[1], str(i + 1), va='center', size=8)

            line.set_label(str(i + 1))
            axes.add_line(line)
            print('dir of ray', dir_of_ray)
            print("A", val.A)
            print("brightness", val.bright)
            print('coords', coords)
            print('line ', i + 1, ' drawed')
            print()


def draw_ray_pool(pool: rays_pool.RaysPool, ray_const_length: float = 2, alpha: float = 1):
    if pool.compon_index_class.DIM != 2:
        raise AttributeError("NON-two-dimensional ray pool")

    for i in range(len(pool)):
        t1 = 1
        if pool.t1(i) != -1:
            t1 = pool.t1(i)
        else:
            t1 = ray_const_length

        coords = collect_point_to_draw(pool.e(i), pool.r(i), pool.t0(i), t1)

        line = pylab.Line2D(coords[0], coords[1], color="green", alpha=alpha)
        axes = pylab.gca()
        axes.add_line(line)


def collect_point_to_draw(e: (list, iter), r: (list, iter), t0: float, t1: float):
    begin = ARay.calc_point_of_ray_(e, r, t0)
    end = ARay.calc_point_of_ray_(e, r, t1)

    x_coor = [begin[0], end[0]]
    y_coor = [begin[1], end[1]]

    return (x_coor, y_coor)


if __name__ == '__main__':
    print(np.sqrt(-1), " ", isinstance(np.sqrt(-1), (float, int)))
    size = 5.5
    pylab.xlim(-size, size)
    pylab.ylim(-size, size)
    pylab.gca().add_line(pylab.Line2D([1, 2], [1, 2]))
    pylab.show()
