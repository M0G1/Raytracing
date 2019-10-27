import numpy as np
from ray.ray import Ray
from surfaces.surface import Surface
from surfaces.plane import Plane
from surfaces.sphere import Sphere
from surfaces.ellipse import Ellipse


def func_of_reading_surf_ray_from_strings(strings, dimension):
    d = dimension
    rays = []
    surfaces = []
    for s in strings:
        nums = np.fromstring(s[3:], dtype=float, count=-1, sep=' ')
        # p = plane s = sphere e = ellipse
        if s[0] == 'r':
            rays.append(Ray(nums[:d], nums[d:2 * d]))
        else:
            surface = None
            if s[0] == 'p':
                if s[1] == 't':
                    surface = Plane(nums[:d], nums[d:2 * d], Surface.types.REFRACTING, nums[len(nums) - 2], nums[len(nums) - 1])
                else:
                    surface = Plane(nums[:d], nums[d:2 * d])
            elif s[0] == 's':
                if s[1] == 't':
                    surface = Sphere(nums[:d], nums[d], Surface.types.REFRACTING, nums[len(nums) - 2], nums[len(nums) - 1])
                else:
                    surface = Sphere(nums[:d], nums[d])
            elif s[0] == 'e':
                if s[1] == 't':
                    surface = Ellipse(nums[:d], nums[d:2 * d], Surface.types.REFRACTING, nums[len(nums) - 2], nums[len(nums) - 1])
                else:
                    surface = Ellipse(nums[:d], nums[d:2 * d])
            if (surface != None):
                print('\tSUCCESS ' + str(surface))
                surfaces.append(surface)

    return rays, surfaces


def read_param_from_file(file, dimension: int):
    strings = file.readlines()
    rays, surfaces = func_of_reading_surf_ray_from_strings(strings, dimension)
    if len(surfaces) == 1:
        surfaces = surfaces[0]
    if len(rays) == 1:
        rays = rays[0]
    return rays, surfaces
