import numpy as np
import math as m

from ray.ray import Ray
from surfaces.surface import Surface
from surfaces.plane import Plane
from surfaces.sphere import Sphere
from surfaces.ellipse import Ellipse

# global values
# incorrect golder ratio ~ 0.381966011 | 1 - i_g_r = 0.6180033989
i_g_r = (3 - m.sqrt(5)) / 2



def func_of_reading_surf_ray_from_strings(strings, dimension):
    d = dimension
    rays = []
    surfaces = []
    for s in strings:
        nums = np.fromstring(s[3:], dtype=float, count=-1, sep=' ')
        # p = plane s = sphere e = ellipse
        if s[0] == 'r':
            rays.append(Ray(nums[:d], nums[d:2 * d]))
        else:
            surface = None
            if s[0] == 'p':
                if s[1] == 't':
                    surface = Plane(nums[:d], nums[d:2 * d], Surface.types.REFRACTING, nums[len(nums) - 2],
                                    nums[len(nums) - 1])
                else:
                    surface = Plane(nums[:d], nums[d:2 * d])
            elif s[0] == 's':
                if s[1] == 't':
                    surface = Sphere(nums[:d], nums[d], Surface.types.REFRACTING, nums[len(nums) - 2],
                                     nums[len(nums) - 1])
                else:
                    surface = Sphere(nums[:d], nums[d])
            elif s[0] == 'e':
                if s[1] == 't':
                    surface = Ellipse(nums[:d], nums[d:2 * d], Surface.types.REFRACTING, nums[len(nums) - 2],
                                      nums[len(nums) - 1])
                else:
                    surface = Ellipse(nums[:d], nums[d:2 * d])
            if (surface != None):
                print('\tSUCCESS ' + str(surface))
                surfaces.append(surface)

    return rays, surfaces


def read_param_from_file(file, dimension: int):
    strings = file.readlines()
    rays, surfaces = func_of_reading_surf_ray_from_strings(strings, dimension)
    if len(surfaces) == 1:
        surfaces = surfaces[0]
    if len(rays) == 1:
        rays = rays[0]
    return rays, surfaces


def min_golden_ratio(f, a: float, b: float, eps: float):
    """
        find param of function where it value is minimal.
        Work only for unimodal function with 1 argument, that returned the float value
    :param f: some unimaodal function with 1 argument, that returned the float value
    :param a: left border of searching
    :param b: right border of searching
    :param eps: search accuracy (positive number)
    :return: tuple of argmin and function value in that point
    """

    x1 = a + i_g_r * (b - a)
    x2 = a + (1 - i_g_r) * (b - a)
    f_x1 = f(x1)
    f_x2 = f(x2)

    while not (abs(b - a) < eps):
        if f_x1 < f_x2:
            b = x2
            x2 = x1
            x1 = a + i_g_r * (b - a)
            f_x2 = f_x1
            f_x1 = f(x1)
        else:
            a = x1
            x1 = x2
            x2 = a + (1 - i_g_r) * (b - a)
            f_x1 = f_x2
            f_x2 = f(x2)

    argmin = (b + a) / 2
    return (argmin, f(argmin))


def reshape_arrays_into_one(*args):
    """
    Arrays must have the same length
    reshape given arrays
    x = [x0,x1,...,xn]
    y = [y0,y1,...,yn]
    ...
    z = [z0,z1,...,zn]
    into
    ans = [x0,y0,...,z0,x1,y1,...,z1,...,xn,yn,zn]


    return numpy.array
    """
    narray = np.array(args)
    return narray.ravel(order='F')


def reshape_array_into_many(arr, row_count, column_count):
    """
    Better to use numpy.reshape(). This method just recall it.
    reshape given array
    arr = [x0,y0,...,z0,x1,y1,...,z1,...,xn,yn,zn]
    into

    x = [x0,x1,...,xn]
    y = [y0,y1,...,yn]
    ...
    z = [z0,z1,...,zn]

    return numpy.array
    """
    return np.reshape(arr, (row_count, column_count), order='F')
