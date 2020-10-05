from ray.rays_pool import RaysPool
from OpenGL import GL
import numpy as np


def draw_ray_pool(rays: RaysPool, color: (list, tuple)):
    for i in range(len(rays)):
        GL.glBegin(GL.GL_LINES)
        GL.glColor(*color)
        begin = rays.begin_ray(i)
        end = rays.end_ray(i)
        GL.glVertex(*begin)
        GL.glVertex(*end)
        GL.glEnd()
