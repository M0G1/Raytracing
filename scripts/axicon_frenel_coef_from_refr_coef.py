from matplotlib import pylab
import time

import opticalObjects.axicon2D as axic
from ray.ray import Ray


def main():
    start = time.time()
    half_angle = 18
    is_isosceles = True
    lenght_of_side_ribs = 3
    is_closed = False
    refr_coef_inside = 1.69
    refr_coef_outsid = 1

    axicon = axic.create_axicon(half_angle, is_isosceles,
                                lenght_of_side_ribs, is_closed,
                                refr_coef_inside, refr_coef_outsid)
    is_single = False
    type_polarization = 'p'
    ray = Ray([-2, 0.2], [1, 0])
    ray_index = 1 if is_single else [1, 3]
    from_refr_coef = 1.696
    to_refr_coef = 1.697
    step = 0.000_000_1

    if is_single:
        single_calculate_frenel_coeff(type_polarization, axicon, ray, ray_index, from_refr_coef, to_refr_coef, step,
                                      start)
    else:
        multiple_calculate_frenel_coeff(type_polarization, axicon, ray, ray_index, from_refr_coef, to_refr_coef, step,
                                        start)


def single_calculate_frenel_coeff(type_polarization, axicon, ray, ray_index, from_refr_coef, to_refr_coef, step,
                                  start):
    func = axic.get_points_of_func_frenel_from_refr_coef(
        type_polarization,
        ray, ray_index,
        axicon,
        [from_refr_coef, to_refr_coef], step
    )
    # приводим данные к привычному формату
    func = ((func[0], func[1]), (func[0], func[2]))

    print("\nCalculated time:", time.time() - start, " sec")

    pylab.figure(1)
    pylab.subplot(2, 1, 1)
    # pylab.title("R(n)")
    pylab.xlabel("Refractive index")
    pylab.ylabel("Reflection coefficient")
    pylab.plot(func[0][0], func[0][1], color='black', label="R(n)")
    pylab.grid(True)

    pylab.subplot(2, 1, 2)
    # pylab.title("T(n)")
    pylab.xlabel("Refractive index")
    pylab.ylabel("Transmittance")
    pylab.plot(func[1][0], func[1][1], color='black')
    pylab.grid(True)

    # search point of intersection
    index_intersetion = 0
    x = 1.69
    y = 0
    eps = 0.001
    for i in range(len(func[0][0])):
        if abs(func[0][1][i] - func[1][1][i]) < eps:
            index_intersetion = i
            x = func[0][0][i]
            y = func[0][1][i]

    pylab.figure(2)
    pylab.title("R(n) and T(n) step(%.4f)" % (step))
    pylab.plot(func[0][0], func[0][1], color='blue', label="R(n)")
    pylab.plot(func[1][0], func[1][1], color='black', label="T(n)")

    pylab.plot([1.69, 1.71], [0.5, 0.5], color='black', label="y =0.5", alpha=0.3)
    pylab.plot([x, x], [0, 1], label="x =%.5f (eps:%.3f)" % (x, eps), color="black", alpha=0.3)

    pylab.legend()
    pylab.grid(True)

    print(f"Working time: {time.time() - start},  sec")
    pylab.show()


def multiple_calculate_frenel_coeff(type_polarization, axicon, ray, ray_indexes, from_refr_coef, to_refr_coef, step,
                                    start):
    x_coor, refl_coef, transmittance = axic.get_points_of_func_frenel(
        type_polarization,
        ray,
        ray_indexes,
        axicon,
        [from_refr_coef, to_refr_coef],
        step
    )
    print("\nCalculated time:", time.time() - start, " sec")

    min_diff = 1000000000000000
    index_min = -1
    for i in range(len(x_coor)):
        diff = abs(transmittance[0][i] - transmittance[1][i])
        if diff < min_diff:
            min_diff = diff
            index_min = i

    max_subplots = len(ray_indexes)
    deep = 4
    refr_coeff = x_coor[index_min]

    pylab.figure(0)
    ans = f"Min diff is={min_diff} n={refr_coeff} 1T={transmittance[0][index_min]},2T={transmittance[1][index_min]}"
    pylab.title(ans)
    print(ans)
    print(ans)
    draw_deep_modeling_trace(type_polarization, axicon, ray, refr_coeff, deep)

    pylab.figure(1)
    for cur_ray_index in range(max_subplots):
        pylab.subplot(max_subplots, 1, cur_ray_index + 1)

        pylab.xlabel("Refractive index")
        pylab.title("R(n) and T(n) step(%.4f) for %i ray" % (step, cur_ray_index + 1))

        pylab.plot(x_coor, refl_coef[cur_ray_index], color='blue', label="R(n)")
        pylab.plot(x_coor, transmittance[cur_ray_index], color='black', label="T(n)")

        pylab.legend()
        pylab.grid(True)

    pylab.figure(2)
    pylab.subplot(2, 1, 1)
    # pylab.title("R(n)")
    pylab.xlabel("Refractive index")
    pylab.ylabel("Reflection coefficient")
    pylab.plot(x_coor, refl_coef[0], color='blue', label="R(n) of 1st ray")
    pylab.plot(x_coor, refl_coef[1], color='black', label="R(n) of 2nd ray")
    pylab.grid(True)

    pylab.subplot(2, 1, 2)
    # pylab.title("T(n)")
    pylab.xlabel("Refractive index")
    pylab.ylabel("Transmittance")
    pylab.plot(x_coor, transmittance[0], color='blue', label="T(n) of 1st ray")
    pylab.plot(x_coor, transmittance[1], color='black', label="T(n) of 2nd ray")
    pylab.grid(True)

    pylab.show()


def draw_deep_modeling_trace(type_polarization, axicon, ray, refr_coef_in_axic, deep):
    import controllers.modeling_controller as modelCtrl
    import view.matlab.matlab_ray_view2D as vray

    # prepare the axicon
    pylab.title("Axicon with refrection index %.7f" % refr_coef_in_axic)
    refraction_indexs = axicon[0].get_refractive_indexes([1, 1])
    refraction_outside_index = refraction_indexs[0]
    for i in axicon:
        i.set_refractive_indexes(refr_coef_in_axic, refraction_outside_index)
    # prepare to draw
    xlim = [-1.6, 0.4]
    ylim = [-1, 1]
    ray_const_lenght = ((xlim[0] - xlim[1]) ** 2 + (ylim[0] - ylim[1]) ** 2) ** 0.5
    # ray_const_lenght = ray_const_lenght/2
    axes = pylab.gca()
    pylab.legend()
    pylab.grid(True)
    pylab.xlim(xlim[0], xlim[1])
    pylab.ylim(ylim[0], ylim[1])

    # trace and draw
    tree = modelCtrl.deep_modeling(type_polarization, ray, axicon, deep)
    for i, subtree in enumerate(tree):
        print(f"{i} - {subtree.value}")
    vray.draw_deep_ray_modeling(tree, axes=axes, color='g',is_real_index=True,ray_const_length=2)
    axic.draw_axicon2D(axicon, axes=axes)

    # return back
    for i in axicon:
        i.set_refractive_indexes(refraction_indexs[1], refraction_outside_index)


if __name__ == '__main__':
    main()
