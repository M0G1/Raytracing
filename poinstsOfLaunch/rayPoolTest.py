import numpy as np
import pylab

import tools.generators as gen
from surfaces.plane import Plane
import ray.rays_pool as rp
import view.MatlabRayView2D as vray

if __name__ == '__main__':
    p1 = [0, 0]
    p2 = [0, 1]
    intensive = 2

    # plane
    n_vec = [1, 0]
    r_vec = [1, 0]

    plane = Plane(r_vec,n_vec)
    pool = gen.Generator.generate_rays_2d(p1, p2, 2)

    print(plane)
    print(pool)

    pylab.xlim(-2,2)
    pylab.ylim(-2,2)
    pylab.grid()
    axes = pylab.gca()

    reflected_pool = pool.reflect(plane)
    print(reflected_pool)

    vray.draw_ray_pool(pool)
    plane.draw_surface(axes)

    pylab.show()
