# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
import OpenGL.GL.shaders
from OpenGL import GL, GLU
from pyrr import matrix44, Matrix44, Vector3

from surfaces.ellipse import Ellipse
from surfaces.sphere import Sphere
from view.opengl.sphere_ellipse_data3D import Sphere_Ellipse_data_3D
from controllers.ray_surface_storage import RaySurfaceStorage
from tools.generators import Generator
from view.opengl.rays_pool import draw_ray_pool


class MyOpenGLWidget(QtWidgets.QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_draw = False
        self.obj = Sphere_Ellipse_data_3D(20, 20)
        arg = self.test_func()
        print(arg)
        print(arg[0][0])
        self.ray_sur_con = RaySurfaceStorage(*arg)
        self.ray_sur_con.trace()
        self.uniform = {}  # set
        self.wireframe = True
        self.line_width = 2

    def test_func(self):
        """Create object """
        center = (2, 0, 0)
        abc = (1.2, 1.1, 1.1)
        surfaces = [Ellipse(center, abc,n1=1.0, n2=1.3)]
        points = ((3, -1, 1),
                  (3, 1, -1),
                  (1, 1, -1))
        intensity = 0.3
        rays = Generator.generate_rays_3d(*points, intensity)
        return [[rays], surfaces]

    def initializeGL(self) -> None:
        GL.glClearColor(0.5, 0.5, 0.5, 0.5)
        light_pos = (-1.0, 0.0, 0.0)
        ambient = (1.0, 1.0, 1.0, 1.0)

        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        GL.glLightModelfv(GL.GL_LIGHT_MODEL_AMBIENT, ambient)  # Определяем текущую модель освещения
        GL.glEnable(GL.GL_LIGHTING)  # Включаем освещение
        GL.glEnable(GL.GL_LIGHT0)  # Включаем один источник света
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_POSITION, light_pos)  # Определяем положение источника света
        self.init_shader()
        # #view projection
        # view = matrix44.create_from_translation(Vector3([0.0, 0.0, -2.0]))
        # projection = matrix44.create_perspective_projection_matrix(45.0, self.aspect_ratio, 0.1, 100.0)
        #
        # vp = matrix44.multiply(view, projection)  # view projection
        #
        # GL.glUniformMatrix4fv(self.uniform["viewProject"],1, GL.GL_FALSE, vp)

    def init_shader(self):
        solo_color_shader_code = """
        # version 330
        
        uniform vec4 vertexesColor;
        out vec4 outColor;
        
        void main()
        {
        outColor = vertexesColor;
        }
        """
        shader = OpenGL.GL.shaders.compileProgram(
            GL.shaders.compileShader(solo_color_shader_code, GL.GL_FRAGMENT_SHADER))
        GL.glUseProgram(shader)
        self.uniform["vertexesColor"] = GL.glGetUniformLocation(shader, "vertexesColor")
        self.uniform["viewProject"] = GL.glGetUniformLocation(shader, "vp")

    def resizeGL(self, w: int, h: int) -> None:
        self.size()
        min_x, max_x, min_y, max_y = (-2, 2, -2, 2)
        # coordinate bounds
        c_b = MyOpenGLWidget._calc_bounds_with_aspect_ratio(w / h, min_x, max_x, min_y, max_y)
        GL.glOrtho(c_b[0], c_b[1], c_b[2], c_b[3], -2, 2)
        GL.glViewport(0, 0, w, h)

    @staticmethod
    def _calc_bounds_with_aspect_ratio(asp_ratio: float, min_x: float, max_x: float, min_y: float, max_y: float):
        midle_x = (min_x + max_x) / 2
        x_range = asp_ratio * (max_y - min_y)
        return midle_x - x_range / 2, midle_x + x_range / 2, min_y, max_y

    def set_drawing_color(self, color: (list, tuple)):
        if len(color) == 4:
            GL.glUniform4f(self.uniform["vertexesColor"], *color)
        elif len(color) == 3:
            GL.glUniform4f(self.uniform["vertexesColor"], *color, 1)

    def paintGL(self) -> None:
        if self.is_draw:
            GL.glLineWidth(self.line_width // 2)
            if self.wireframe:
                GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)
            else:
                GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)

            self.set_drawing_color((50, 0, 0))
            print(f"\ncount of RaysPool is {len(self.ray_sur_con.rays)}\n")
            for rays in self.ray_sur_con.rays:
                draw_ray_pool(rays, (1, 0, 0, 1))
                # print(rays)

            GL.glLineWidth(self.line_width)
            self.set_drawing_color((0, 50, 0, 1))
            for surface in self.ray_sur_con.surfaces:
                if isinstance(surface, (Sphere, Ellipse)):
                    self.obj.draw_in_opengl(surface, True)
