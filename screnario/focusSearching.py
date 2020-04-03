import pylab
import numpy as np
import math as m

from surfaces.ellipse import Ellipse
from ray.rays_pool import RaysPool
from surfaces.limited_surface import LimitedSurface
from tools.generators import Generator

import tools.help as help
import controllers.rayPoolmodelingCtrl as rpmc
import view.MatlabSurfaceView2D as msv
import view.MatlabRayView2D as mvray


def average(points: (list, tuple, iter)) -> np.ndarray:
    """
    :param points: list of same dimensional point
    :return: average point for list of point
    """
    p_aver = [0] * len(points[0])
    for point in points:
        p_aver = np.add(p_aver, point)

    return np.divide(p_aver, len(points))


def get_sco_func(rays_pools: (tuple, list), refr_coef: float):
    """
    Before use it methods you need calculate optical path in all RaysPool except last.
    The optical path must be calculating for ray in RaysPool and they must be same length
    :param rays_pools: list of RaysPool
    (length of iterable objects rays_pools and refr_coef must to match)
    :param refr_coef: refraction coefficient for last RaysPool in rays_pools
    :return: function of sco for searching focus
    """
    if not all(isinstance(val, RaysPool) for val in rays_pools):
        raise AttributeError("Some element in argument ray_pool is not instance of RaysPool class")
    # if not all(isinstance(val, (int, float)) and val > 0 for val in refr_coef):
    #     raise AttributeError("Some element in argument refr_coef is not real positive number")
    # if len(rays_pools) != len(refr_coef):
    #     raise AttributeError(
    #         "Different length of rays_pools(%s) and refr_coef(%s)" % (str(len(rays_pools)), str(len(refr_coef))))

    # optical path of ray
    # read from down to up
    ray_opt_paths = [
        [
            rays_pools[i].l(j)
            for j in range(len(rays_pools[i]))
        ]
        for i in range(len(rays_pools) - 1)
    ]
    #     calc const
    ray_path_const = ray_opt_paths[0]
    for i in range(1, len(ray_opt_paths)):
        ray_path_const = np.add(ray_path_const, ray_opt_paths[i])

    # define variables
    last_pool: RaysPool = rays_pools[len(rays_pools) - 1]
    # del some variables
    del ray_opt_paths
    print("ray_path_const", ray_path_const)

    # write the answer function in vector form

    def r(h: float):
        """
        :param last_pool: RayPool with not parallel rays
        :param ray_path_const: sum of optical path others RaysPool
        :param h: length of ray
        :return: list of point
        """
        # read from down to up
        # ans = []
        # for i in range(len(last_pool)):
        #     step = (h - ray_path_const[i]) / refr_coef
        #     val = last_pool.calc_point_of_ray(i, step)
        #     ans.append(val)
        # return ans
        return [last_pool.calc_point_of_ray(i, (h - ray_path_const[i]) / refr_coef) for i in range(len(last_pool))]

        # return [last_pool.calc_point_of_ray(i, h) for i in range(len(last_pool))]

    def ans(h: float):
        """
        This function used to calculate the sco of rays for length rays equal h
        : param h: length rays
        : return: sco of rays for length rays equal h
        """
        # point for ray length - h
        p_ray = r(h)
        # average point (I don't sure that work)
        p_aver = average(p_ray)
        sco = 0
        for point in p_ray:
            p_sub = np.subtract(p_aver, point)
            sco = sco + np.matmul(p_sub, p_sub)
        return m.sqrt(sco / len(p_ray))

    return (ans, r)


if __name__ == '__main__':
    # surface preparation
    ab_1 = [0.8, 3]
    ab_2 = [1, 3]
    ab_s = [ab_1, ab_2]

    r0 = 0.5
    center2 = [0, 0]
    center1 = [center2[0] + r0, center2[0]]
    center_s = [center1, center2]

    # n1 - outside n2 - inside
    n1 = 1
    n2 = 1.33

    ellipsis = [Ellipse(center_s[i], ab_s[i], Ellipse.types.REFRACTING, n1=n1, n2=n2) for i in range(2)]

    y_lim = 2.8
    limits1 = [[center1[0] - ab_1[0], center1[0]], [-y_lim, y_lim]]
    limits2 = [[center2[0], center2[0] + ab_2[0]], [-y_lim, y_lim]]
    limits = [limits1, limits2]

    lim_ell = [LimitedSurface(ellipsis[i], limits[i]) for i in range(2)]

    for lim_surface in lim_ell:
        print(lim_surface)

    # raysPool preparation
    points = [
        [-1.1, -1],
        [-1.1, 1]
    ]
    intensity = 5.5

    pool = Generator.generate_rays_2d(points[0], points[1], intensity)

    # modeling and calculating optical path
    # pools = rpmc.tracing_rayspool_ordered_surface(pool, lim_ell)
    pools = rpmc.tracing_rayspool_ordered_surface(pool, lim_ell, is_set_optical_path=True)
    # find the refraction coefficient(refractive_indexes) there goes the last RaysPool
    # index 0 and length 0.1 are random
    last_RaysPool: RaysPool = pools[len(pools) - 1]
    point = last_RaysPool.calc_point_of_ray(0, 0.1)
    refr_coef = lim_ell[len(lim_ell) - 1].get_refractive_indexes(point)[0]

    print("refr_coef(%s) = %s" % (str(point), str(refr_coef)))

    sco_f, r1 = get_sco_func(pools, refr_coef)
    # minimize the sco
    # params a and b are random!!!!!
    accuracy = 0.01
    h, val = help.min_golden_ratio(sco_f, 0, 100, accuracy)

    print("optical length of last RaysPool: %f\nsco in that point: %f with accuracy: %f" % (h, val, accuracy))

    points = r1(h)
    focus_point = average(points)

    # # test
    # f = lambda x: x ** 2
    # print("test", help.min_golden_ratio(f, -1, 2, 10 ** -2))
    # # test

    # drawing
    pylab.figure(0, figsize=(5, 5))

    # focus point
    xy = [[points[j][i] for j in range(len(points))] for i in range(2)]
    pylab.scatter(xy[0], xy[1], color="red", marker='.', alpha=0.5)
    pylab.scatter(focus_point[0], focus_point[1], color="purple", marker="*")

    # surfaces
    for lim_surface in lim_ell:
        msv.draw_exist_surface(lim_surface, "purple", 1)

    for ellipse in ellipsis:
        msv.draw_exist_surface(ellipse)

    print()

    # rays pools
    for ray_pool in pools:
        mvray.draw_ray_pool(ray_pool, ray_const_length=18, alpha=0.2)
        print(ray_pool)

    # config the view

    pylab.grid()
    a = 8
    lim = max(np.abs([2 + a]))

    shift = (0 + a, 0)
    lim_x = (-lim + shift[0], lim + shift[0])
    lim_y = (-lim + shift[1], lim + shift[1])

    pylab.xlim(lim_x[0], lim_x[1])
    pylab.ylim(lim_y[0], lim_y[1])

    pylab.show()
# 1/f = (n2/n1 -1)(1/r1 + 1/r2) -где r1,r2 радиусы кривизны(отрицательны елси вогнутая относительно одного направления)
# 1/f = 0.33(1 - 0.5) = 0.165 f=6.06
