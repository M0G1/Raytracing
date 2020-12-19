import pylab
import numpy as np
import math as m
from typing import List

from surfaces.ellipse import Ellipse
from ray.rays_pool import RaysPool
from surfaces.limited_surface import LimitedSurface
from tools.generators import Generator

import tools.help as help
import controllers.ray_pool_ctrl as rpmc
import view.matlab.matlab_surface_view2D as msv
import view.matlab.matlab_ray_view2D as mvray


def average(points: (list, tuple, iter)) -> np.ndarray:
    """
    :param points: list of same dimensional point
    :return: average point for list of point
    """
    p_aver = np.zeros(len(points[0]))
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
        raise ValueError("Some element in argument ray_pool is not instance of RaysPool class")
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
    ray_path_const = np.zeros(len(ray_opt_paths[0]))
    for i in range(len(ray_opt_paths)):
        ray_path_const = np.add(ray_path_const, ray_opt_paths[i])

    # define variables
    last_pool: RaysPool = rays_pools[len(rays_pools) - 1]
    # del some variables
    del ray_opt_paths
    print("ray_path_const", ray_path_const)
    print(f"\nmax of ray_path_const {np.max(ray_path_const)}\n")

    # write the answer function

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


def len_width_on_main_axis(list_ellips: (tuple, list)):
    """
        Ellipses must be on abscissa axis(X)
        The first ellipse must have a center right than the second one
    """

    return (list_ellips[1].center[0] + list_ellips[1].abc[0]) - (list_ellips[0].center[0] - list_ellips[0].abc[0])


def sco_from_z(z: np.array, surfaces, begin_of_rays_on_z: float, r) -> (np.array, list, np.ndarray):
    """
        z - some linspace of axis z. All z must begin after last surfaces. Z is the axis along which the rays go.
        surfaces - ellipses, what center is on z=0  and y=0 line. It must be sorted in order of ray going.
            Pair of ellipses is a lens
        begin_of_rays_on_z:float - the coordinate of z. The rays must begin before all surfaces.
        r - function, what returned the end points of ray for given optical path r(h)
            see function get_sco_func

        return values of sco for linspace of axis z
    """
    if any([not isinstance(surface, LimitedSurface) for surface in surfaces]):
        raise ValueError

    if any([not isinstance(surface.surface, Ellipse) for surface in surfaces]):
        raise ValueError

    length_of_medium = np.zeros(len(surfaces))
    optical_destiny = np.zeros(len(surfaces))
    ctrl_point = np.zeros(surfaces[0].dim)
    cur_z = begin_of_rays_on_z
    next_z = None
    for i, surface in enumerate(surfaces):
        if i == 0:
            ctrl_point[0] = begin_of_rays_on_z
        else:
            if i % 2 == 0:
                ctrl_point[0] = (cur_z + (surface.surface.center[0] - surface.surface.abc[0])) / 2
            else:
                ctrl_point[0] = surface.surface.center[0]
        optical_destiny[i] = surface.get_refractive_indexes(ctrl_point)[0]

        if i % 2 == 0:
            next_z = surfaces[i].surface.center[0] - surfaces[i].surface.abc[0]
            length_of_medium[i] = next_z - cur_z
        else:
            ellipses = (surfaces[i - 1].surface, surfaces[i].surface)
            len_width = len_width_on_main_axis(ellipses)
            length_of_medium[i] = len_width
            next_z = len_width + cur_z
        cur_z = next_z

    # print(f"\nlength_of_medium \n{length_of_medium}")
    # print(f"\noptical_destiny \n{optical_destiny}")

    # found the full optical path along the axis
    # # optical path with help of scalar mul
    const_l = np.dot(length_of_medium, optical_destiny)
    ctrl_point[0] += (surfaces[len(surfaces) - 2].surface.abc[0] + 1)
    optical_destiny_last_medium = surfaces[len(surfaces) - 2].get_refractive_indexes(ctrl_point)[0]
    L = (z - cur_z) * optical_destiny_last_medium + const_l

    r_arr = [r(l_el) for l_el in L]
    r_average = np.average(r_arr, axis=1)

    sco = np.zeros(len(z))
    for i in range(len(L)):
        p_sub = r_average[i] - r_arr[i]
        for j in range(len(p_sub)):
            sco[i] += np.dot(p_sub[j], p_sub[j])

    return np.sqrt(sco / len(r_arr[0])), L


DELTA = 1e-15
DELTA_2 = np.array((-DELTA, DELTA))

if __name__ == '__main__':
    # surface preparation
    ab_1_1 = (0.8, 3)
    ab_1_2 = (1, 3)
    ab_2_1 = (0.8, 3)
    ab_2_2 = (1, 3)
    ab_s = [ab_1_1, ab_1_2, ab_2_1, ab_2_2]

    # distance between centers
    r0_1 = 0.5
    r0_2 = 0.5
    dis_bet_lens = 1  # distance between lens
    # illustration
    #   /          \                  /          \
    #   \---r0_1---/---dis_bet_lens---\---r0_2---/
    #    1         2                  3         4
    #    0         1                  2         3 - indexs
    #   ----------------------------------------> X axis
    center2 = (0, 0)
    center1 = (center2[0] + r0_1, 0)
    center4 = (center2[0] + ab_s[1][0] + dis_bet_lens + ab_s[3][0], 0)
    # center4 = (center1[0] + ab_s[1][0] + dis_bet_lens + ab_s[3][0], 0)# Think about it
    center3 = (center4[0] + r0_2, 0)
    center_s = (center1, center2, center3, center4)

    # n1 - outside of len, n2 - inside of len, n3 - inside of len.
    n1 = 1
    n2 = 1.33
    n3 = 1.33
    n_len = (n2, n3)

    ellipsis = [Ellipse(center_s[i], ab_s[i], Ellipse.types.REFRACTING, n1=n1, n2=n_len[i // 2]) for i in range(4)]

    y_lim_1 = 2.8  # coordinate Y where 2 ellipse intersect
    y_lim_2 = 2.8
    limits1 = ((center1[0] - ab_s[0][0], center1[0]), (-y_lim_1, y_lim_1))
    limits2 = ((center2[0], center2[0] + ab_s[1][0]), (-y_lim_1, y_lim_1))
    limits3 = ((center3[0] - ab_s[2][0], center3[0]), (-y_lim_2, y_lim_2))
    limits4 = ((center4[0], center4[0] + ab_s[3][0]), (-y_lim_2, y_lim_2))
    limits = [limits1, limits2, limits3, limits4]
    limits = DELTA_2 + limits  # make borders more a little. VERY IMPORTANT

    lim_ell = [LimitedSurface(ellipsis[i], limits[i]) for i in range(4)]

    for lim_surface in lim_ell:
        print(lim_surface)

    # ------------- preview of surface for debug --------------
    is_need_view_custom = False
    if is_need_view_custom:
        print(f"len_width is {len_width_on_main_axis(ellipsis[:2])}")
        pylab.figure(404, figsize=(5, 5))
        for lim_surface in lim_ell:
            msv.draw_exist_surface(lim_surface, "purple", 1)

        for ellipse in ellipsis:
            msv.draw_exist_surface(ellipse)
        pylab.grid()
        distanse_from_border = 0.1
        b_max = np.max([ab_s[i][1] for i in range(4)])
        a_max = np.max([ab_s[i][0] for i in range(4)])
        y_inf = np.min([center_s[i][1] for i in range(4)]) - b_max - distanse_from_border
        y_sup = np.max([center_s[i][1] for i in range(4)]) + b_max + distanse_from_border
        x_inf = np.min([center_s[i][0] for i in range(4)]) - a_max - distanse_from_border
        x_sup = np.max([center_s[i][0] for i in range(4)]) + a_max + distanse_from_border

        pylab.xlim(x_inf, x_sup)
        pylab.ylim(y_inf, y_sup)
        pylab.show()

    # ___________________________________________________________

    # raysPool preparation
    y_abs = 1
    gen_ray_points = [
        [-1.1, -y_abs],
        [-1.1, y_abs]
    ]
    intensity = 5.5

    pool = Generator.generate_rays_2d(gen_ray_points[0], gen_ray_points[1], intensity)

    # modeling and calculating optical path
    # pools = rpmc.tracing_rayspool_ordered_surface(pool, lim_ell)
    pools = rpmc.tracing_rayspool_ordered_surface(pool, lim_ell, is_set_optical_path=True)
    # find the refraction coefficient(refractive_indexes) there goes the last RaysPool
    last_RaysPool: RaysPool = pools[len(pools) - 1]
    # index 0 and length DELTA = 0.1 are random
    DELTA = 0.1
    point = last_RaysPool.calc_point_of_ray(0, DELTA)
    refr_coef = lim_ell[len(lim_ell) - 1].get_refractive_indexes(point)[0]

    print("refr_coef(%s) = %s" % (str(point), str(refr_coef)))

    sco_f, r1 = get_sco_func(pools, refr_coef)
    # minimize the sco
    # params a and b are random!!!!!
    accuracy = 0.00001
    h, val = help.min_golden_ratio(sco_f, 0, 100, accuracy)

    print("optical length of last RaysPool: %f\nsco in that point: %f with accuracy: %f" % (h, val, accuracy))

    h_ch = h - 0.01
    points = r1(h)
    focus_point = average(points)
    sco = sco_f(h)
    print(f"\nfocus_point:  {focus_point}\nsco is {sco}")

    points2 = r1(h_ch)
    focus_point2 = average(points2)
    sco2 = sco_f(h_ch)

    print(f"focus_point2:  {focus_point2}\nsco is {sco2}")

    shift_in_sco_plot = 0.1
    opt_path = np.linspace(h - shift_in_sco_plot, h + shift_in_sco_plot, 20)
    sco_arr = [sco_f(cur_path) for cur_path in opt_path]

    fig_num = 0

    print(last_RaysPool)


    def draw(limits, points, focus_point):
        global fig_num
        # drawing
        pylab.figure(fig_num, figsize=(6, 5))
        fig_num = fig_num + 1
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

        # config the view
        pylab.grid()

        pylab.xlim(*limits[0])
        pylab.ylim(*limits[1])


    distanse_from_border = 0.1
    b_max = np.max([ab_s[i][1] for i in range(4)])
    a_max = np.max([ab_s[i][0] for i in range(4)])
    y_inf = np.min([center_s[i][1] for i in range(4)]) - b_max - distanse_from_border
    y_sup = np.max([center_s[i][1] for i in range(4)]) + b_max + distanse_from_border
    x_inf = np.min([center_s[i][0] for i in range(4)]) - a_max - distanse_from_border
    x_sup = np.max([center_s[i][0] for i in range(4)]) + a_max + distanse_from_border

    h_tab = np.linspace(10, 12, 50)
    r_arr = [r1(h_tab_el) for h_tab_el in h_tab]
    print(r_arr)
    r_average = [average(r_arr_el)[0] for r_arr_el in r_arr]

    print(f"")
    z = np.linspace((focus_point[0] - shift_in_sco_plot), (focus_point[0] + shift_in_sco_plot))
    sco_z, L = sco_from_z(z, lim_ell, gen_ray_points[0][0], r1)
    l_sum = 0
    for i in range(len(pools)):
        j = len(pools[i]) // 2
        if i < len(pools) - 1:
            l_sum += pools[i].l(j)
        print(f"e {pools[i].e(j)}, r {pools[i].r(j)}, t0 {pools[i].t0(j)},  t1 {pools[i].t1(j)},  l {pools[i].l(j)}")

    print(f"\nopt path {l_sum}")
    lim_x_sco_min = focus_point[0] - 3 * sco
    lim_x_sco_max = focus_point[0] + 3 * sco
    lim_y_sco_min = focus_point[1] - 2 * sco
    lim_y_sco_max = focus_point[1] + 2 * sco

    # draw(((x_inf, x_sup), (y_inf, y_sup)), points, focus_point)
    draw(((x_inf, x_sup + 6.2), (y_inf, y_sup)), points, focus_point)
    pylab.title("Ray density: %.1f, focus at (%.3f,%3.f)" % (intensity, *focus_point))
    draw(((lim_x_sco_min, lim_x_sco_max), (lim_y_sco_min, lim_y_sco_max)), points, focus_point)
    pylab.title(f"Count of ray is {len(points)}, sco is {sco}")
    # draw(((10.1, 10.2), (-0.05, 0.05)), points, focus_point)
    # draw(((10.1, 10.2), (-0.05, 0.05)), points2, focus_point2)

    pylab.figure(fig_num + 1)
    pylab.plot(opt_path, sco_arr)
    pylab.scatter(h, sco, color="red", marker='*', alpha=0.5)
    pylab.title(f"Dependence of SCO from optical path")
    # pylab.scatter(h_ch, sco2, color="red", marker='.', alpha=0.5)
    pylab.grid()

    pylab.figure(fig_num + 2)
    pylab.plot(h_tab, r_average)
    pylab.plot(L, z, color="r")
    pylab.grid()
    pylab.title("Dependence of average from optical path")

    pylab.figure(fig_num + 3)
    pylab.plot(r_average, h_tab)
    pylab.plot(z, L, color="r")
    pylab.grid()
    pylab.title("Dependence of z from optical path")

    pylab.figure(fig_num + 4)
    pylab.plot(z, sco_z)
    pylab.title("Dependence of sco from coordinate abscissa")
    pylab.grid()

    pylab.show()
    # 1/f = (n2/n1 -1)(1/r1 + 1/r2) -где r1,r2 радиусы кривизны(отрицательны елси вогнутая относительно одного направления)
    # 1/f = 0.33(1 - 0.5) = 0.165 f=6.06
