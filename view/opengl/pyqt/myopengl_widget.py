# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
import OpenGL.GL.shaders
from OpenGL import GL, GLU

from surfaces.ellipse import Ellipse
from view.opengl.sphere_ellipse_data3D import Sphere_Ellipse_data_3D


class MyOpenGLWidget(QtWidgets.QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_draw = False
        self.obj = Sphere_Ellipse_data_3D(20, 20)
        center = (2, 0, 0)
        abc = (1.2, 1.0, 1)
        self.surface = Ellipse(center, abc)
        self.uniform = {}  # set
        self.wireframe = True
        self.line_width = 2

    def initializeGL(self) -> None:
        GL.glClearColor(1., 1.0, 1., 0.5)
        light_pos = (-1.0, 0.0, 0.0)
        ambient = (1.0, 1.0, 1.0, 1.0)

        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        GL.glLightModelfv(GL.GL_LIGHT_MODEL_AMBIENT, ambient)  # Определяем текущую модель освещения
        GL.glEnable(GL.GL_LIGHTING)  # Включаем освещение
        GL.glEnable(GL.GL_LIGHT0)  # Включаем один источник света
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_POSITION, light_pos)  # Определяем положение источника света
        self.init_shader()

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
        GL.glColor(1.0, 1.0, 1.0, 1.0)
        if self.is_draw:
            GL.glLineWidth(self.line_width)
            if self.wireframe:
                GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)
            else:
                GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)

            self.set_drawing_color((0, 50, 0))
            self.obj.draw_in_opengl(self.surface, True)
