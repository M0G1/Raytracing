import numpy as np
import pylab

import tools.generators as gen
from surfaces.plane import Plane
from surfaces.sphere import Sphere
from surfaces.sphere import Surface
from surfaces.limited_surface import LimitedSurface
import ray.rays_pool as rp
import view.MatlabRayView2D as vray
import view.MatlabSurfaceView2D as msv

if __name__ == '__main__':
    p1 = [0, -1.9]
    p2 = [-0.1, 1.9]
    intensive = 2

    # plane
    n_vec = [1, 0]
    r_vec = [1, 0]

    plane = Plane(r_vec, n_vec)
    sphere = Sphere([3, 0], 2, Surface.types.REFRACTING, 1, 1.3, )

    pool = gen.Generator.generate_rays_2d(p1, p2, intensive)

    print("\n", plane, "\n")
    print(pool, "\n")

    pylab.xlim(-0.5, 7.5)
    pylab.ylim(-4, 4)
    pylab.grid()
    axes = pylab.gca()

    reflected_pool = pool.refract(sphere)
    refr_refr_pool = reflected_pool.refract(sphere)
    print(reflected_pool)

    print("\n", sphere, "\n")
    lim = [[1.5, 4.5], [-1, 1]]
    print("lim", lim, "\n")

    vray.draw_ray_pool(pool)
    vray.draw_ray_pool(reflected_pool)
    vray.draw_ray_pool(refr_refr_pool)
    msv.draw_sphere(sphere, axes)

    limited = LimitedSurface(sphere, lim)
    # msv.draw_limited_ellipse(limited)
    # msv.draw_limited_ellipse(limited,axes)

    # a = [(2, 1), (2, 1), (0, 2), (2 * np.pi, 2), (1, 3), (2 * np.pi - 1, 3)]
    # print(a)
    # b = dict(a)
    # print(b)
    # c = list(b.keys())
    # print(c)
    # print(c.sort())
    pylab.show()
