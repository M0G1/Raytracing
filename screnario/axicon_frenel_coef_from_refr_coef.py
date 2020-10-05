from matplotlib import pylab
import time

import opticalObjects.axicon2D as axic
from ray.ray import Ray

if __name__ == '__main__':
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
    type_polarization = 'p'
    ray = Ray([-2, 0.2], [1, 0])
    ray_index = 1
    from_refr_coef = 1.69
    to_refr_coef = 1.71
    step = 0.0001

    func = axic.get_points_of_func_frenel_from_refr_coef(
        type_polarization,
        ray, ray_index,
        axicon, ray_index + 1,
        [from_refr_coef, to_refr_coef], step
    )
    # приводим данные к привычному формату
    func = ((func[0], func[1]), (func[0], func[2]))

    print("\nCalculated time:", time.time() - start, " sec")

    pylab.figure(1)
    pylab.subplot(2, 1, 1)
    # pylab.title("R(n)")
    # pylab.xlabel("Refractive index")
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

    print("Worked time:", time.time() - start, " sec")
    pylab.show()
