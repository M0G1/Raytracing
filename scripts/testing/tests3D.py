import numpy as np
import math as m
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import controllers.modeling_controller as mctrl
from surfaces.plane import Plane
from ray.ray import Ray
from surfaces.ellipse import Ellipse
from tools.generators import Generator
from controllers.ray_surface_storage import RaySurfaceStorage


def ellipse(axes, abc: list, center: list = [0, 0, 0], color='b', alpha=0.5):
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)

    x = np.subtract(abc[0] * np.outer(np.cos(u), np.sin(v)), -center[0])
    y = np.subtract(abc[1] * np.outer(np.sin(u), np.sin(v)), -center[1])
    z = np.subtract(abc[2] * np.outer(np.ones(np.size(u)), np.cos(v)), -center[2])

    axes.plot_surface(x, y, z, rstride=4, cstride=4, color=color, alpha=alpha)


def line(axes, x, y, z, color='b'):
    axes.plot(x, y, z, label='LINE', color=color)


def d_plane(axes, plane: Plane, color='b', alpha=0.5):
    pi_2 = m.pi / 2
    M = Generator.get_rot_mat_3d(pi_2, pi_2, pi_2)
    norm = plane.norm_vec([])
    r = plane.rad
    rotated_n = np.dot(M[1], norm)
    points = [np.dot(M[2], rotated_n)]
    for i in range(3):
        points.append(np.dot(M[2], points[i]))
    else:
        for i in range(4):
            points[i] = points[i] + r

    xyz = [
        [[], []],
        [[], []],
        [[], []]
    ]
    for i in range(2):
        for j in range(3):
            xyz[j][0].append(points[i][j])

    for i in range(3, 1, -1):
        for j in range(3):
            xyz[j][1].append(points[i][j])

    axes.plot_surface(
        np.asarray(xyz[0]), np.asarray(xyz[1]), np.asarray(xyz[2]),
        rstride=4, cstride=4, color=color, alpha=alpha)


def points(axes, x, y, z, color='b', marker='o'):
    axes.scatter(x, y, z, c='b', marker='o')


def main():
    center = [1, 2, 1]
    abc = [1, 1, 1]
    ray: Ray = Ray([0, 0, 0], [1, 1, 1])
    ellipse1 = Ellipse(center=center, ellipse_coefficients=abc, type_surface=Ellipse.types.REFRACTING, n1=1, n2=1.33)
    plane = Plane([1, 1, 1], [0, 1, 1], type_surface=Ellipse.types.REFRACTING, n1=1, n2=1.33)

    # way_point_of_ray = mctrl.model_path(ray, [ellipse1], is_have_ray_in_infinity=True)
    way_point_of_ray2 = mctrl.model_path(ray, [plane], is_have_ray_in_infinity=True)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

    # ellipse(ax, ellipse1.abc, ellipse1.center)
    # line(ax, way_point_of_ray[0], way_point_of_ray[1], way_point_of_ray[2], "g")
    line(ax, way_point_of_ray2[0], way_point_of_ray2[1], way_point_of_ray2[2], "g")
    d_plane(ax, plane)

    plt.show()


def main2():
    center = [1, 2, 1]
    abc = [1, 1, 1]
    ellipse1 = Ellipse(center=center, ellipse_coefficients=abc, type_surface=Ellipse.types.REFRACTING, n1=1, n2=1.33)
    points = ((0.1, 1.1, 0.1),
              (0.1, 2.9, 1.9),
              (1.9, 2.9, 0.1))
    intensity = 0.1
    rays = Generator.generate_rays_3d(*points, intensity)

    a = RaySurfaceStorage([rays], [ellipse1])
    a.trace()


if __name__ == '__main__':
    main2()
