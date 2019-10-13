# -*- coding: utf-8 -*-
import logging
from tools import help as h
import pylab


def log(func):
    """
    Логируем какая функция вызывается.
    """

    def wrap_log(*args, **kwargs):
        name = func.__name__
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)

        # Открываем файл логов для записи.
        fh = logging.FileHandler("%s.log" % name)
        fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        formatter = logging.Formatter(fmt)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        logger.info("function call: %s" % name)
        result = func(*args, **kwargs)
        logger.info("Result: %s" % result)
        return func

    return wrap_log


@log
def double_function(a):
    """
    Умножаем полученный параметр.
    """
    return a * 2


# ======main===========================================================================

file = open("input1.txt")
rays, surfaces = h.read_param_from_file(file, 2)
file.close()

if isinstance(rays, list):
    for i in rays:
        print(str(i))
else:
    print(str(rays))

if not isinstance(surfaces, list):
    temp = [surfaces]
    surfaces = temp

for i in surfaces:
    print(str(i))

print()

for i in range(len(surfaces)):
    arr_char = "intersection of " + str(surfaces[i]) \
               + " and " + str(rays) + ": "
    arr_char += str(surfaces[i].find_nearest_point_intersection(rays))
    print(arr_char)

# test

pylab.grid()
# Получим текущие оси
axes = pylab.gca()
axes.set_aspect("equal")
# максимальный размер осей
size = 15
pylab.xlim(-size, size)
pylab.ylim(-size, size)

print("\n\tsurfaces draw:")
for sur in surfaces:
    print(str(sur.__class__) + " " + str(sur.draw_surface(axes)))

way_points_of_ray = rays.path_ray(surfaces)
way_on_point = [[i, j] for i, j in zip(way_points_of_ray[0], way_points_of_ray[1])]
print("way of ray " + str(way_on_point))
rays.draw_ray(axes, way_points_of_ray)
pylab.show()
# Some problems with path_of_ray
#
# except ...:
#     print("SOME WENT WRONG")
# finally:
#     file.close()
#     print("END OF PROGRAM")
