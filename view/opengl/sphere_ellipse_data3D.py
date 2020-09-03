"""
Module for generate data of sphere and ellipse to drawing. And to drawing in openGl
"""

import math

import numpy as np
from OpenGL import GL

import tools.help
from surfaces.sphere import Sphere
from surfaces.ellipse import Ellipse

from view.opengl.gen_id_buff_and_arrays import GenId
from view.opengl.np_gl_manage_types import NP_GL_Types


class Sphere_Ellipse_data_3D:
    def __init__(self, sector_count=50, stack_count=50, np_gl_types: NP_GL_Types = NP_GL_Types()):
        """
            realization from https: // songho.ca / opengl / gl_sphere.html
            param sector_count:
            param digit_capacity: digit capacity of data for drawing in openGL
        """
        self.stack_count = stack_count  # count of rows
        self.sector_count = sector_count  # count of columns

        self.vertexes = None
        self.normals = None
        self.tex_coords = None
        self.vao_sphere = None
        self.indexes = None
        self.is_init_data = False  # vertexes array
        self.is_init_opengl_data = False  # index array, normals, tex coords
        self.is_prepared = False  # is create/bind/fill glBuffers and glArrays
        self.np_gl_t = np_gl_types  # for works with types of opengl and numpy

        self.ebo_sphere = None

    def init_data(self):
        self.vertexes = self.get_sphere_vertexes3D()
        # flag self.is_init_data is True

    def init_opengl_data(self):
        if self.is_init_data:
            self.normals = self.vertexes.copy
        else:
            self.vertexes = self.gen_approximate_sphere()
        self.tex_coords = self._make_text_coords()
        self.indexes = self._make_incidents_vertexes_to_opengl()
        self.is_init_opengl_data = True
        # print(np.reshape(self.vertexes, (3, self.sector_count * self.stack_count), order='F'))
        # print(self.indexes)

    # =================================|generating and data getting|================================================
    def gen_approximate_sphere2(self):
        # did from there, but on python: https: // songho.ca / opengl / gl_sphere.html
        vertexes = []
        sector_step = 2 * math.pi / (self.sector_count)
        stack_step = math.pi / (self.stack_count)

        for i in range(self.stack_count + 1):
            stack_angle = math.pi / 2 - i * stack_step
            xy = math.cos(stack_angle)
            z = math.sin(stack_angle)
            for j in range(self.sector_count + 1):
                sector_angle = j * sector_step
                x = xy * math.cos(sector_angle)
                y = xy * math.sin(sector_angle)
                vertexes.append(x)
                vertexes.append(y)
                vertexes.append(z)
        return np.array(vertexes, dtype=self.np_gl_t.npf)

    def gen_approximate_sphere(self):
        # do like there, but on python: https: // songho.ca / opengl / gl_sphere.html

        stack_angles = np.linspace(math.pi / 2, -math.pi / 2, self.stack_count + 1)  # , dtype=self.np_gl_t.npf)
        sector_angles = np.linspace(0, 2 * math.pi, self.sector_count + 1)  # , dtype=self.np_gl_t.npf)

        xy = np.cos(stack_angles)  # , dtype=self.np_gl_t.npf)
        z = np.sin(stack_angles)  # , dtype=self.np_gl_t.npf)
        cos_sec = np.cos(sector_angles)  # , dtype=self.np_gl_t.npf)
        sin_sec = np.sin(sector_angles)  # , dtype=self.np_gl_t.npf)

        # len(xy) elements are same dot. It repeats twice
        # make grid of coordinates
        x = np.outer(xy, cos_sec)
        y = np.outer(xy, sin_sec)
        z = np.outer(z, np.ones(self.sector_count + 1))

        x = np.ravel(x)
        y = np.ravel(y)
        z = np.ravel(z)

        temp = tools.help.reshape_arrays_into_one(x, y, z)
        return np.array(temp, dtype=self.np_gl_t.npf)

    def get_sphere_vertexes3D(self):
        """It is change the state of variable vertexes.
            Use for initialise
        """
        if self.is_init_data:
            return self.vertexes
        self.vertexes = self.gen_approximate_sphere()
        self.is_init_data = True
        return self.vertexes

    def _make_text_coords(self):
        # do like there, but on python: https: // songho.ca / opengl / gl_sphere.html
        s = np.linspace(0, 1, self.sector_count + 1)  # for column
        t = np.linspace(0, 1, self.stack_count + 1)  # for row

        t = np.outer(t, np.ones(self.sector_count + 1))
        s = np.outer(np.ones(self.stack_count + 1), s)

        return tools.help.reshape_arrays_into_one(s, t)

    def get_tex_coords(self):
        if self.tex_coords:
            return self.tex_coords
        self.tex_coords = self._make_text_coords()
        return self.tex_coords

    def scale(self, a=1, b=1, c=1):
        """
        scale inner variable vertexes
        # try to use opengl func scale
        """
        reshapes_arr = np.reshape(self.vertexes, (self.stack_count + 1, self.sector_count + 1), order='F')
        x = a * reshapes_arr[0]
        y = b * reshapes_arr[1]
        z = c * reshapes_arr[2]
        self.vertexes = tools.help.reshape_arrays_into_one(x, y, z)
        return self.vertexes

    # =================================|opengl usage|==================================================================

    def _make_incidents_vertexes_to_opengl(self):
        # done it like there, but on python: https: // songho.ca / opengl / gl_sphere.html

        incidents = []
        k1, k2 = None, None
        for i in range(self.stack_count):
            k1 = i * (self.sector_count + 1)  # beginning of current stack
            k2 = k1 + self.sector_count + 1  # beginning of next stack
            for j in range(self.sector_count):
                # 2 triangles per sector excluding first and last stacks
                # k1 => k2 => k1+1 Contre clock wise
                if i != 0:
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
        # set the most suitable integer type
        self.np_gl_t.set_integer_types(len(incidents))
        return np.array(incidents, dtype=self.np_gl_t.npi)

    def _prepare_to_draw(self):
        """
        Create buffer, binding buffer and copy in buffer data. For more fast works of app.

        """
        print(self.np_gl_t.npf)
        if not self.is_init_opengl_data:
            self.init_opengl_data()

        self.vao_sphere = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.vao_sphere)
        vbo_sphere = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo_sphere)
        GL.glBufferData(GL.GL_ARRAY_BUFFER,
                        len(self.vertexes) * self.np_gl_t.sizeof_f,
                        self.vertexes,
                        GL.GL_STATIC_DRAW)

        # element buffer object
        self.ebo_sphere = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.ebo_sphere)
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER,
                        self.indexes.itemsize * len(self.indexes),
                        self.indexes,
                        GL.GL_STATIC_DRAW)
        # vertex attribute pointer
        # # zero? may be it is an ID
        # # 3 vertex coor
        # # normilase = false
        # # next vertex position in bites
        # # GL.ctypes.c_void_p(0) - number of bites in array there beginning the vertex
        GL.glVertexAttribPointer(0, 3, self.np_gl_t.glf, GL.GL_FALSE,
                                 3 * self.np_gl_t.sizeof_f,
                                 GL.ctypes.c_void_p(0))
        GL.glEnableVertexAttribArray(0)
        # # unbind  sphere vao
        # GL.glBindVertexArray(0)

        self.is_prepared = True

    def __del__(self):
        self._end_of_draw()

    def _end_of_draw(self):
        if self.is_prepared:
            # unbind indexes
            GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
            # unbind sphere vao
            GL.glBindVertexArray(0)

            self.is_prepared = False

    def draw_sphere(self, is_stay_prepared=False):
        """
        Drawing the current sphere in opengl
        is_stay_prepared: save the prepared state to draw the next sphere or ellipse
        """
        if not self.is_prepared:
            self._prepare_to_draw()
        GL.glColor(135, 1, 1, 0.5)
        # GL.glBindVertexArray(self.vao_sphere)
        GL.glDrawElements(GL.GL_TRIANGLES, len(self.indexes), self.np_gl_t.gli, None)
        if not is_stay_prepared:
            self._end_of_draw()

    def draw_in_opengl(self, surface: (Ellipse, Sphere), is_stay_prepared=False):
        """draw the sphere in open gl"""
        GL.glPushMatrix()

        GL.glTranslate(*surface.center)  # auto unpacking arg
        if isinstance(surface, Ellipse):
            GL.glScale(*surface.abc)

        self.draw_sphere(is_stay_prepared=is_stay_prepared)
        GL.glPopMatrix()


def main():
    obj = Sphere_Ellipse_data_3D(25, 50)
    obj2 = Sphere_Ellipse_data_3D(30, 30)
    d = {obj: GenId.get_some_value(obj), obj2: GenId.get_some_value(obj2)}
    print(f"op: {d[obj]}", f"op2: {d[obj2]}")
    print(f"ou: {GenId.get_some_value(obj)}", f"ou2: {GenId.get_some_value(obj2)}")

    obj3 = Sphere_Ellipse_data_3D(5, 5, np_gl_types=NP_GL_Types(64))
    var_a = obj3.gen_approximate_sphere()
    var_b = obj3.gen_approximate_sphere2()
    var_c = np.reshape(var_b, (3, var_b.size // 3), order="F")
    var_d = np.reshape(var_a, (3, var_a.size // 3), order="F")
    i = 4
    i = i + 1
    # obj3.draw_sphere(None)

    sub = np.subtract(var_a, var_b)
    print(f"sub {sub}, max {np.max(sub)}")


if __name__ == '__main__':
    main()
