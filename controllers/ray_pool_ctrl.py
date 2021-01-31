import numpy as np
from typing import NewType, Any, List, Tuple, Callable

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
    old_rays_pool = pool
    for i, surface in enumerate(surfaces):
        # may be i wanna to do some other here(searching of index)
        new_rays_pool = None
        if surface.type == Surface.types.REFLECTING:
            new_rays_pool = old_rays_pool.reflect(surface)
        elif surface.type == Surface.types.REFRACTING:
            new_rays_pool = old_rays_pool.refract(surface)

        if new_rays_pool is None:
            break
        # Last RaysPool don't have the optical path
        if is_set_optical_path:
            # # take the rays in the middle of RaysPool (take 0 simpler)
            # num = len(old_rays_pool) // 2
            # t1 = old_rays_pool.t1(num)
            # # the case then  t1 = -1. It mean that ray haven't the intersection with surface
            # if t1 == -1:
            #     continue
            t = (old_rays_pool.t1(0) - old_rays_pool.t0(0)) / 2
            n1, n2 = surface.get_refractive_indexes(old_rays_pool.calc_point_of_ray(0, t))

            for j in range(len(old_rays_pool)):
                l_i = (old_rays_pool.t1(j) - old_rays_pool.t0(j)) * n1

                old_rays_pool.set_l(j, l_i)
        ans.append(new_rays_pool)
        old_rays_pool = new_rays_pool
    else:
        print("\tAll surfaces have been passed(%d)" % (len(surfaces)))
    return ans


def tracing_rayspool_ordered_surface_with_add_opt(pool: RaysPool, surfaces: (tuple, iter, list), is_check: bool = False,
                                                  add_functions: Tuple[Callable] = tuple(), *args, **kwargs):
    """
    Tracing the ray throw the surfaces with added options.
    All rays in one pool must interact with one surface
    :param pool: object of class RaysPool
    :param surfaces: list of surfaces arranged in series.
        The refractive indices of surfaces must be correct.
        Between two surfaces there should be one and the same coefficient in each of them (surfaces)
    :param add_functions additional function for setting some fields within RaysPool.
        For each function, an instance of one surface and two a ray pool (old and new) is passed from the tuple.
        All other positional(*args) and named(**kwargs) arguments are also passed there

    Example of signature one of  additional function:
    def some_action(surface:Surface, old_pool:RaysPool, new_pool:RaysPool):
        # old pool is a falling on surface beams
        # new pool is a created by falling beams new rays
        # some action with surface and RaysPool

    :return: list of RaysPool s or None if some is wrong
    """
    if is_check:
        if any(not isinstance(surface, Surface) for surface in surfaces):
            raise AttributeError("Some element of surfaces is not instance of Surface: " + str(surfaces))

    ans = [pool]
    old_rays_pool = pool
    for i, surface in enumerate(surfaces):
        # may be i wanna to do some other here(searching of index)
        new_rays_pool = None
        if surface.type == Surface.types.REFLECTING:
            new_rays_pool = old_rays_pool.reflect(surface)
        elif surface.type == Surface.types.REFRACTING:
            new_rays_pool = old_rays_pool.refract(surface)

        if new_rays_pool is None:
            break

        for fu in add_functions:
            fu(surface, old_rays_pool, new_rays_pool, *args, **kwargs)

        ans.append(new_rays_pool)
        old_rays_pool = new_rays_pool
    else:
        print("\tAll surfaces have been passed(%d)" % (len(surfaces)))
    return ans


def set_optical_path(surface: Surface, old_pool: RaysPool, new_pool: RaysPool):
    # # take the rays in the middle of RaysPool (take 0 simpler)
    # num = len(old_rays_pool) // 2
    # t1 = old_rays_pool.t1(num)
    # # the case then  t1 = -1. It mean that ray haven't the intersection with surface
    # if t1 == -1:
    #     continue
    t = (old_pool.t1(0) - old_pool.t0(0)) / 2
    n1, n2 = surface.get_refractive_indexes(old_pool.calc_point_of_ray(0, t))

    for j in range(len(old_pool)):
        l_i = (old_pool.t1(j) - old_pool.t0(j)) * n1

        old_pool.set_l(j, l_i)


def change_ray_polar_state(surface: Surface, old_pool: RaysPool, new_pool: RaysPool):
    for i in range(len(old_pool)):
        polar_mat = None
        if surface.type == Surface.types.REFLECTING:
            polar_mat = surface.polar_matrix_relect
        elif surface.type == Surface.types.REFRACTING:
            polar_mat = surface.polar_matrix_refract

        new_polar_state = polar_mat.get_new_polar_state(old_pool.jones_vec(i))
        new_pool.set_jones_vec(i, new_polar_state)
