import numpy as np


def is_2d_complex_vector(vec: (np.array, list, tuple)):
    if len(vec) != 2:
        return False
    if any([not isinstance(vec[i], (float, int, complex)) for i in range(2)]):
        return False
    return True


def get_param_ellipse_polar(vec: (np.array, list, tuple), is_need_check=True):
    """
        vec - Jones vector(two dimensional vector with complex numbers) double precision
        Return (alpha,Beta)

        alpha - polarization ellipse azimuth.   -pi/2 <= alpha <= pi/2
        beta - angle of ellipticity.            -pi/4 <= beta <= pi/4

        sing of beta show direction of polarization.
        For positive beta - right polarisation.
        For negative - left polarisation.

        Еhe vector electric field strength rotates clockwise for an observer
        looking in the opposite direction of radiation propagation,
        then the polarization is called right elliptical, else left.
    """
    if is_need_check:
        if not is_2d_complex_vector(vec):
            raise ValueError(f"Argument vec {vec} is not Jones vector")
    if np.all(np.absolute(np.array(vec)) < np.finfo(np.float_).eps):
        raise ValueError(f"All components of Vec {vec} equal 0")

    xi: complex = complex(0, 0)
    alpha = 0
    if abs(vec[0]) > np.finfo(np.float_).eps:
        xi: complex = vec[1] / vec[0]
    else:
        alpha = (np.pi / 2) * (-1) ** (int(xi.real < 0))

    abs_xi = np.absolute(xi)
    if abs_xi > np.finfo(np.float_).eps:
        print(f"vec {vec}\nxi={xi}, polar coord={(abs_xi, np.angle(xi))}")
        if np.abs(abs_xi - 1) > np.finfo(np.float_).eps * 10:
            arg = 2 * xi.real / (1 - abs_xi ** 2)
            print(arg)
            alpha = np.arctan(arg) / 2
        else:
            # component A_X equal zero
            # handle tg(+-1/0)=tg(+-inf)
            alpha = (np.pi / 2) * (-1) ** (int(xi.real < 0))
        print()

    beta = np.arcsin(2 * xi.imag / (1 + abs_xi ** 2)) / 2
    return (alpha, beta)
