# -*- coding: utf-8 -*-
import logging
import pylab

from utility import help as h
import controllers.modeling_controller as mCTRL
import view.matlab.matlab_ray_view2D as view


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
if __name__ == '__main__':

    file = open("input_data.txt")
    rays, surfaces = h.read_param_from_file(file, 2)
    file.close()

    pylab.grid()
    # Получим текущие оси
    axes = pylab.gca()
    axes.set_aspect("equal")
    # максимальный размер осей
    size = 5.5
    pylab.xlim(-size, size)
    pylab.ylim(-size, size)

    print("\n\tsurfaces draw:")
    for sur in surfaces:
        print(str(sur.__class__) + " " + str(sur.draw_surface(axes)))

    way_points_of_ray =  mCTRL.path_ray_for_drawing(rays, surfaces,is_have_ray_in_infinity=True)
    way_on_point = [[i, j] for i, j in zip(way_points_of_ray[0], way_points_of_ray[1])]
    print("way of ray " + str(way_on_point))
    view.draw_ray(axes, way_points_of_ray, color='green')

    pylab.show()
    # Some problems with path_of_ray
    #
    # except ...:
    #     print("SOME WENT WRONG")
    # finally:
    #     file.close()
    #     print("END OF PROGRAM")
