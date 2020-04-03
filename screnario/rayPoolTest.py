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
import controllers.rayPoolmodelingCtrl as rpmc

if __name__ == '__main__':
    p1 = [0, -1.9]
    p2 = [0, 1.9]
    intensive = 1

    # plane
    n_vec = [1, -1]
    r_vec = [0, 0]

    plane = Plane(r_vec, n_vec)
    sphere = Sphere([3, 0], 2, Surface.types.REFRACTING, 1, 1.3, )

    lim = [[1, 3.9], [-1, 1]]
    print("lim", lim, "\n")
    print(plane)

    limited = LimitedSurface(sphere, lim)
    lim_plane = LimitedSurface(plane, lim)

    pool = gen.Generator.generate_rays_2d(p1, p2, intensive)

    print("\n", plane, "\n")
    print(sphere)

    pools = rpmc.tracing_rayspool_ordered_surface(pool, (sphere, sphere),is_set_optical_path=True)
    for pool_i in pools:
        vray.draw_ray_pool(pool_i)
        print(pool_i)

    msv.draw_sphere(sphere)
    msv.draw_exist_surface(lim_plane, color="pink", alpha=1)
    msv.draw_exist_surface(limited, color="red")
    msv.draw_limits(lim_plane)
    # msv.draw_limited_ellipse(limited,axes)

    shift = [3, 0]
    max = abs(np.max(lim)) + 2
    pylab.xlim(-max + shift[0], max + shift[0])
    pylab.ylim(-max + shift[1], max + shift[1])
    pylab.grid()
    pylab.show()
