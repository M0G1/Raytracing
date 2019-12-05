import numpy as np
import pylab

from ray.ray import Ray
from surfaces.plane import Plane
from surfaces.limited_surface import LimitedSurface
from surfaces.surface import Surface
import controllers.modelingController as modelCtrl
import view.MatlabRayView2D as vray


def is_correct_angle(angle) -> bool:
    if angle <= 0 or angle >= 90:
        print("Oops. You should be thoughtful")
        return False
    return True


def is_correct_length(len) -> bool:
    if len <= 0:
        print("Oops. You should be thoughtful")
        return False
    return True


def read_param():
    isosceles = input("Is it isosceles triangle(y/n)?")
    if isosceles is 'y' or isosceles is 'Y':
        isosceles = True
    else:
        isosceles = False
    ans = input("Do you want to enter param in console or use file(c - console/f - file)?")
    angle = None
    length = None
    rayarr = None
    refr_coef = None
    if ans[0] is 'c' or ans[0] is 'C':
        angle = float(input("Enter the angle of line( 0 < angle < 90).\n"))
        if not is_correct_angle(angle):
            return

        length = float(input("Enter the length of hypotenuse(length > 0)\n"))
        if not is_correct_length(length):
            return
        refr_coef = input("Enter refraction coefficients. N1 - inside triangle. N2 - outside('n1 n2')\n")
        refr_coef = [float(s) for s in refr_coef.split(' ')]
        if len(refr_coef) is not 2:
            print("Oops. You should be thoughtful")
            return
        raystr = input("And most difficult. Enter the ray(begin of ray and direction \'x1 y1 x2 y2\')\n")
        rayarr = [float(s) for s in raystr.split(' ')]
        if len(rayarr) is not 4:
            print("Oops. You should read carefully. And think about it. I sad you that it is difficult.")
            return
    elif ans[0] is 'f' or ans[0] is 'F':
        filename = input(
            "Enter path to file('filename.txt') or enter the 'd' to use default file('pic.txt')")
        if filename is 'd':
            filename = "pic.txt"
        file = open(filename)
        angle = float(file.readline())
        length = float(file.readline())
        refr_coef = file.readline()
        print(refr_coef)
        refr_coef = [float(val) for val in refr_coef.split(' ')]
        print(refr_coef)
        raystr = file.readline()
        rayarr = [float(s) for s in raystr.split(' ')]
        if not is_correct_angle(angle):
            return
        if not is_correct_length(length):
            return
        if len(refr_coef) is not 2:
            print("Oops. You should read carefully. And think about it. I sad you that it is difficult.")
            return
        if len(rayarr) is not 4:
            print("Oops. You should read carefully. And think about it. I sad you that it is difficult.")
            return
    else:
        return
    angle = angle * np.pi / 180
    sinA = np.sin(angle)
    cosA = -np.cos(angle)
    dir_vec = [cosA, sinA]
    x, y = [val * length for val in dir_vec]
    m = [[0, -1],
         [1, 0]]
    norm = list(np.dot(dir_vec, m))
    print(refr_coef)
    line1 = Plane([0, 0], norm, Surface.types.REFRACTING, n1=refr_coef[0], n2=refr_coef[1])
    line2 = None
    if isosceles:
        norm2 = norm.copy()
        norm2[1] *= -1
        line2 = Plane([0, 0], norm2, Surface.types.REFRACTING, n1=refr_coef[0], n2=refr_coef[1])
    else:
        line2 = Plane([0, 0], [0, -1], Surface.types.REFRACTING, n1=refr_coef[0], n2=refr_coef[1])
    limits1 = [[x, 0],
               [0, y]]
    limits2 = [[x, 0],
               [-y, 0]]
    ray = Ray(rayarr[:2], rayarr[2:4])
    line1 = LimitedSurface(line1, limits1)
    line2 = LimitedSurface(line2, limits2)
    return [ray, line1, line2, [x, y], isosceles]


arg = read_param()
if arg is not None:
    ray = arg[0]
    surfaces = arg[1:3]
    for i in arg:
        print(str(i))

    # size = 5
    # pylab.xlim(arg[3][0] - 1, 1)
    # pylab.ylim(-(arg[3][1] + 1), arg[3][1] + 1)
    pylab.xlim(-3, 3)
    pylab.ylim(-3, 3)

    pylab.grid()
    axes = pylab.gca()
    tree = modelCtrl.deep_modeling(ray, surfaces, 4)
    for node in tree:
        print(str(node.value) + str(node.value._Ray__path_of_ray))
    vray.draw_deep_ray_modeling(tree=tree, axes=axes, color='g')

    # line = pylab.Line2D([-1, 1], [1, 1], color='green',label="lllllllllllllline")
    # axes.add_line(line)
    l1 = pylab.Line2D([arg[3][0], 0], [arg[3][1], 0])
    l2 = None
    l3 = None
    if arg[4]:
        l2 = pylab.Line2D([arg[3][0], 0], [-arg[3][1], 0])
        l3 = pylab.Line2D([arg[3][0], arg[3][0]], [arg[3][1], -arg[3][1]])
    else:
        l3 = pylab.Line2D([arg[3][0], arg[3][0]], [arg[3][1], 0])
        l2 = pylab.Line2D([arg[3][0], 0], [0, 0])
    axes.add_line(l3)
    axes.add_line(l2)
    axes.add_line(l1)
    axes.legend()

    pylab.show()
