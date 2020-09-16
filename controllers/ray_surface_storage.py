from collections import Iterable

from surfaces.surface import Surface
from ray.rays_pool import RaysPool
import controllers.ray_pool_ctrl as rpmc


class RaySurfaceStorage():
    """This is a global storage of data for application"""

    def __init__(self, rays: (list, tuple), surfaces: (list, tuple)):
        if not all(isinstance(val, RaysPool) for val in rays):
            raise AttributeError("Rays have not instanced RaysPool value")
        if not all(isinstance(val, Surface) for val in surfaces):
            raise AttributeError("Rays have not instanced RaysPool value")
        self.rays = rays
        self.surfaces = surfaces

    def trace(self):
        self.rays = rpmc.tracing_rayspool_ordered_surface(self.rays[0], self.surfaces)

