"""
Module for generate data of sphere and ellipse to drawing. And to drawing in openGl
"""

import math

import numpy as np

import tools.help


class Sphere_Ellipse_data_3Dview:

    def __init__(self, sector_count=50, stack_count=50, is_lazy=True):
        self.stack_count = stack_count  # count of rows
        self.sector_count = sector_count  # count of columns
        self.is_lazy = True

        self.vertexes = None
        self.normals = None
        self.tex_coords = None

        if not is_lazy:
            self.vertexes = self.get_sphere_vertexes3D()
            self.normals = self.vertexes.copy
            self.tex_coords = self.make_text_coords()

    def gen_approximate_sphere(self):
        # do like there, but on python: https: // songho.ca / opengl / gl_sphere.html

        stack_angles = np.linspace(math.pi / 2, -math.pi / 2, self.stack_count)
        sector_angles = np.linspace(0, 2 * math.pi, self.sector_count)

        xy = np.cos(stack_angles)
        z = np.sin(stack_angles)
        cos_sec = np.cos(sector_angles)
        sin_sec = np.sin(sector_angles)

        # len(xy) elements are same dot. It repeats twice
        # make grid of coordinates
        x = np.outer(xy, cos_sec)
        y = np.outer(xy, sin_sec)
        z = np.outer(z, np.ones(self.sector_count))

        x = np.ravel(x)
        y = np.ravel(y)
        z = np.ravel(z)

        return tools.help.reshape_arrays_into_one(x, y, z)

    def get_sphere_vertexes3D(self):
        """It is change the state of variable vertexes.
            Use for initialise
        """
        if self.vertexes:
            return self.vertexes
        self.vertexes = self.gen_approximate_sphere()
        return self.vertexes

    def make_text_coords(self):
        # do like there, but on python: https: // songho.ca / opengl / gl_sphere.html
        s = np.linspace(0, 1, self.sector_count)
        t = np.linspace(0, 1, self.stack_count)

        return tools.help.reshape_arrays_into_one(s, t)

    def get_tex_coords(self):
        if self.tex_coords:
            return self.tex_coords
        self.tex_coords = self.make_text_coords()
        return self.tex_coords

    def scale(self, a=1, b=1, c=1):
        """
        scale inner variable vertexes
        # try to use opengl func scale
        """
        reshapes_arr = np.reshape(self.vertexes, (self.stack_count, self.sector_count), order='F')
        x = a * reshapes_arr[0]
        y = b * reshapes_arr[1]
        z = c * reshapes_arr[2]
        self.vertexes = tools.help.reshape_arrays_into_one(x, y, z)
        return self.vertexes

    def get_incidents_vertexes_to_opengl(self):
        # do like there, but on python: https: // songho.ca / opengl / gl_sphere.html

        incidents = []
        k1, k2 = None, None
        for i in range(self.stack_count):
            k1 = i * (self.sector_count + 1)  # beginning of current stack
            k2 = k1 + self.sector_count + 1  # beginning of next stack

            for j in range(self.sector_count):
                # 2 triangles per sector excluding first and last stacks
                # k1 => k2 => k1+1 Contre clock wise
                if i is not 0:
                    incidents.append(k1)
                    incidents.append(k2)
                    incidents.append(k1 + 1)
                if i is not (self.sector_count - 1):
                    incidents.append(k1 + 1)
                    incidents.append(k2)
                    incidents.append(k2 + 1)

                # increment indexes
                k1 += 1
                k2 += 1

        return np.array(incidents)


def main():
    obj = Sphere_Ellipse_data_3Dview(25, 50)
    obj.get_sphere_vertexes3D()


if __name__ == '__main__':
    main()
