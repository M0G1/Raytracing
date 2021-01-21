import numpy as np

from surfaces.additional.polar_mat import PolarMat
from tools.generators import Generator


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


def main():
    polar_mat_test()


if __name__ == '__main__':
    main()
