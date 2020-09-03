# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from OpenGL import GL, GLU

from surfaces.ellipse import Ellipse
from view.opengl.sphere_ellipse_data3D import Sphere_Ellipse_data_3D


class MyOpenGLWidget(QtWidgets.QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_draw = False
        self.obj = Sphere_Ellipse_data_3D(50, 50)
        center = (2, 0, 0)
        abc = (1.2, 1.0, 1)
        self.surface = Ellipse(center, abc)
        self.aspect_ratio = self.size().width() / self.size().height()
        self.wireframe = True

    def initializeGL(self) -> None:
        GL.glClearColor(1., 1.0, 1., 0.5)
        light_pos = (-1.0, 0.0, 0.0)
        ambient = (1.0, 1.0, 1.0, 1.0)

        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        GL.glLightModelfv(GL.GL_LIGHT_MODEL_AMBIENT, ambient)  # Определяем текущую модель освещения
        GL.glEnable(GL.GL_LIGHTING)  # Включаем освещение
        GL.glEnable(GL.GL_LIGHT0)  # Включаем один источник света
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_POSITION, light_pos)  # Определяем положение источника света

    def resizeGL(self, w: int, h: int) -> None:
        self.size()
        self.aspect_ratio = w / h
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

    def paintGL(self) -> None:
        GL.glColor(1.0, 1.0, 1.0, 1.0)
        if self.is_draw:
            if self.wireframe:
                GL.glPolygonMode(GL.GL_FRONT_AND_BACK,GL.GL_LINE)
            else:
                GL.glPolygonMode(GL.GL_FRONT_AND_BACK,GL.GL_FILL)

            self.obj.draw_in_opengl(self.surface, True)
