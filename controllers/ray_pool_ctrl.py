import numpy as np

from surfaces.surface import Surface
from ray.rays_pool import RaysPool


def tracing_rayspool_ordered_surface(pool: RaysPool, surfaces: (tuple, iter, list), is_check: bool = False,
                                     is_set_optical_path: bool = False):
    """
    Tracing the ray throw the surfaces.
    All rays in one pool must interact with one surface
    :param pool: object of class RaysPool
    :param surfaces: list of surfaces arranged in series.
    The refractive indices of surfaces must be correct.
    Between two surfaces there should be one and the same coefficient in each of them (surfaces)
    :return: list of RaysPool s or None if some is wrong
    """
    if is_check:
        if any(not isinstance(surface, Surface) for surface in surfaces):
            raise AttributeError("Some element of surfaces is not instance of Surface: " + str(surfaces))

    ans = [pool]
    new_rays_pool = pool
    for i, surface in enumerate(surfaces):
        # may be i wanna to do some other here(searching of index)
        temp = None
        if surface.type == Surface.types.REFLECTING:
            temp = new_rays_pool.reflect(surface)
        elif surface.type == Surface.types.REFRACTING:
            temp = new_rays_pool.refract(surface)

        if temp is None:
            break
        # Last RaysPool don't have the optical path
        if is_set_optical_path:
            # # take the rays in the middle of RaysPool (take 0 simpler)
            # num = len(new_rays_pool) // 2
            # t1 = new_rays_pool.t1(num)
            # # the case then  t1 = -1. It mean that ray haven't the intersection with surface
            # if t1 == -1:
            #     continue
            t = (new_rays_pool.t1(0) - new_rays_pool.t0(0)) / 2
            n1, n2 = surface.get_refractive_indexes(new_rays_pool.calc_point_of_ray(0, t))

            for j in range(len(new_rays_pool)):
                l_i = (new_rays_pool.t1(j) - new_rays_pool.t0(j)) * n1

                new_rays_pool.set_l(j, l_i)
        ans.append(temp)
        new_rays_pool = temp
    else:
        print("\tAll surfaces have been passed(%d)" % (len(surfaces)))
    return ans
