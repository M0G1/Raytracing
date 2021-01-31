import numpy as np
import pylab

from surfaces.additional.polar_mat import PolarMat
from tools.generators import Generator
from surfaces.plane import Plane
from controllers import ray_pool_ctrl as rpc
from view.matlab import matlab_surface_view2D as surface_view, matlab_ray_view2D as ray_view
from view.matlab import polarization


def polar_mat_test():
    trans_mat = [[2, 0],
                 [0, 1]]
    pol_mat = PolarMat(trans_mat)

    rot_mat_x_ccw = lambda a: Generator.get_rot_mat_2d(a)
    rot_mat_x_cw = lambda a: Generator.get_rot_mat_2d(-a)

    pol_mat.add_dependence_from_param(("a",), "left", rot_mat_x_ccw)
    # pol_mat.add_dependence_from_param(("a",), "right", rot_mat_x_cw)

    for i in np.linspace(0, np.pi, 5):
        print(i)
        print(pol_mat.get_polar_mat(a=i), "\n")


def tracing():
    # make pool
    points = ((-1, -1),
              (-0.9, 1))
    pool = Generator.generate_rays_2d(points[0], points[1], 5.)
    vec_jonson = [1, 1]
    for i in range(len(pool)):
        pool.set_jones_vec(i, vec_jonson)

    # make plane
    norm = [1, 0]
    start = [0, 0]
    n1, n2 = 1, 1.33
    polar_mat = PolarMat(Generator.get_rot_mat_2d(np.pi / 2))
    plane = Plane(start, norm, type_surface=Plane.types.REFRACTING, n1=n1, n2=n2)
    plane.polar_matrix_refract = polar_mat
    surfaces = (plane,)

    # make param for tracing method
    add_functions = (rpc.change_ray_polar_state,)
    # trace
    pool_list = rpc.tracing_rayspool_ordered_surface_with_add_opt(pool, surfaces, False, add_functions)

    # drawing

    #   scene
    pylab.figure(0)
    #       surfaces
    for surface in surfaces:
        surface_view.draw_exist_surface(surface)
    #       rays
    for pool_to_draw in pool_list:
        ray_view.draw_ray_pool(pool_to_draw)
    pylab.grid()
    pylab.xlim(-2, 4)
    pylab.ylim(-2, 2)
    pylab.title("Polarized light passed throw polarising surface")
    pylab.show()

    # polar state for every pool
    for i in range(len(pool_list)):
        pylab.figure(2 + i)
        vec_jo_to_draw = pool_list[i].jones_vec(0)
        title = f"Polar state for {i + 1} bean\n" + polarization.get_str_view_polar_vec(vec_jo_to_draw)
        polarization.draw_polar_ellipse(vec_jo_to_draw, title=title)
        pylab.grid()

    pylab.show()


def main():
    # polar_mat_test()
    tracing()


if __name__ == '__main__':
    main()
