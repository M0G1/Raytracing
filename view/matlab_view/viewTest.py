import numpy as np
import pylab

from surfaces.plane import Plane
from view.matlab_view.sphere_ellipse_data2D import Sphere_Ellipse_data_2Dview
import view.matlab_view.matlab_surface_view2D as vsur

from surfaces.ellipse import Ellipse
from surfaces.limited_surface import LimitedSurface


def test1():
    a = 1
    b = 2
    ab = (a, b)
    is_ellipse = True
    step = 0.01
    center = (1, 2)

    to_draw = Sphere_Ellipse_data_2Dview.get_ellipse2D(step, center, ab)
    pylab.plot(to_draw[0], to_draw[1])
    pylab.plot(to_draw[0], to_draw[1])

    max = np.max(2)
    pylab.xlim(-max + center[0], max + center[0])
    pylab.ylim(-max + center[1], max + center[1])

    pylab.grid()
    pylab.show()


def test2():
    a = 1
    b = 2
    ab = (a, b)
    is_ellipse = True
    step = 0.01
    center = (0, 0)

    ell = Ellipse(center, ab)

    limits = ((-1, 0.5), (-1, 1))
    planes = [
        Plane([limits[0][0], 0], [1, 0]),
        Plane([limits[0][1], 0], [1, 0]),
        Plane([0, limits[1][0]], [0, 1]),
        Plane([0, limits[1][1]], [0, 1])
    ]
    # vsur.draw_ellipse(ell, axes=pylab.gca())
    # for plane in planes:
    #     vsur.draw_plane(plane,  color="black")

    lim_ell = LimitedSurface(ell, limits)

    vsur.draw_limited_ellipse(lim_ell,color="green",alpha=1)

    pylab.grid()
    max = np.max(2)
    pylab.xlim(-max + center[0], max + center[0])
    pylab.ylim(-max + center[1], max + center[1])

    pylab.show()


if __name__ == '__main__':
    test2()
