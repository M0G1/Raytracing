from collections import Iterable

from surfaces.surface import Surface
from ray.rays_pool import RaysPool


class RaySurfaceStorage():
    """This is a global storage of data for application"""

    def __init__(self, rays: Iterable, surfaces: Iterable):
        self.rays = rays
        self.surfaces = surfaces
