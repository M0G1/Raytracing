import sys
import time
import math
import tkinter as tk

import numpy as np
from OpenGL import GL, GLU, GLUT
from pyopengltk import OpenGLFrame


class MyOpenGLFrame(OpenGLFrame):

    def __init__(self, *args, drawing_methods=None, **kwargs):
        super.__init__(*args, **kwargs)

        if drawing_methods:
            self.__drawing_methods = drawing_methods
        else:
            self.__drawing_methods = []

    @property
    def drawing_methods(self):
        """Variable for storing  methods using openGL to image.
        Put here only python methods
        """
        return self.__drawing_methods

    @drawing_methods.setter
    def drawing_methods(self, value):
        self.__drawing_methods = value

    def initgl(self):
        self.draw_from_list()

    def draw_from_list(self):
        """Execute methods in drawing methods"""
        for m in self.__drawing_methods:
            m()
        return

