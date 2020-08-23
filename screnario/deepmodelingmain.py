import pylab

from ray.ray import Ray
import controllers.modeling_controller as modelCtrl
import view.matlab_view.matlab_ray_view2D as vray
import opticalObjects.axicon2D as axicon
import time


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
    auto_run = True
    isosceles = True
    if not auto_run:
        isosceles = input("Is it isosceles triangle(y/n)?")
        if isosceles is 'y' or isosceles is 'Y':
            isosceles = True
        else:
            isosceles = False
    # ans = input("Do you want to enter param in console or use file(c - console/f - file)?")
    angle = None
    length = None
    rayarr = None
    refr_coef = None
    filename = None
    # if ans[0] is 'c' or ans[0] is 'C':
    #     angle = float(input("Enter the angle of line( 0 < angle < 90).\n"))
    #     if not is_correct_angle(angle):
    #         return
    #
    #     length = float(input("Enter the length of hypotenuse(length > 0)\n"))
    #     if not is_correct_length(length):
    #         return
    #     refr_coef = input("Enter refraction coefficients. N1 - inside triangle. N2 - outside('n1 n2')\n")
    #     refr_coef = [float(s) for s in refr_coef.split(' ')]
    #     if len(refr_coef) is not 2:
    #         print("Oops. You should be thoughtful")
    #         return
    #     raystr = input("And most difficult. Enter the ray(begin of ray and direction \'x1 y1 x2 y2\')\n")
    #     rayarr = [float(s) for s in raystr.split(' ')]
    #     if len(rayarr) is not 4:
    #         print("Oops. You should read carefully. And think about it. I sad you that it is difficult.")
    #         return
    # elif ans[0] is 'f' or ans[0] is 'F':
    # filename = input(
    #     "Enter path to file('filename.txt') or enter the 'd' to use default file('pic.txt')")
    # if filename is 'd':
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
    # else:
    #     return

    ray = Ray(rayarr[:2], rayarr[2:4])
    axic = axicon.create_axicon(angle, isosceles, length, False, refr_coef[0], refr_coef[1])
    return [ray, axic[0], axic[1], isosceles, angle]


start = time.time()
arg = read_param()
if arg is not None:
    ray = arg[0]
    surfaces = arg[1:3]
    for i in arg:
        print(str(i))

    # size = 5
    # pylab.xlim(arg[3][0] - 1, 1)
    # pylab.ylim(-(arg[3][1] + 1), arg[3][1] + 1)
    # pylab.xlim(-3, 0.4)
    xlim = [-1.6, 0.4]
    ylim = [-1, 1]
    ray_const_lenght = ((xlim[0] - xlim[1])**2 + (ylim[0] - ylim[1])**2)**0.5
    # ray_const_lenght = ray_const_lenght/2

    pylab.xlim(xlim[0], xlim[1])
    pylab.ylim(ylim[0], ylim[1])

    pylab.grid()
    axes = pylab.gca()

    tree = modelCtrl.deep_modeling('p', ray, surfaces, 4, ray_const_length=ray_const_lenght)
    for node in tree:
        print(str(node.value) + str(node.value._Ray__path_of_ray))

    for node in tree:
        print(str(node.value))

    vray.draw_deep_ray_modeling(tree=tree, axes=axes, color='g', lower_limit_brightness=0.07)
    axicon.draw_axicon2D(surfaces, axes, arg[3])
    refr_index = surfaces[0].get_refractive_indexes([-1, 0])
    # pylab.title(
    #     "Axicon\nhalf angle: =%f \nrefractive indexs: inside: %f, outside: %f" % (arg[4], refr_index[0], refr_index[1]),
    #     alpha=0.7)

    pylab.title(
        "Axicon \nrefractive indexs inside: %.4f\nrefractive indexs outside: %.4f" % (refr_index[0], refr_index[1]),
        alpha=0.7)
    axes.legend()

    print("Worked time:", time.time() - start, " sec")
    pylab.show()
