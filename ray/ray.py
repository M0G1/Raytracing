import numpy as np
import pylab

from surfaces.surface import Surface
import math as m
from utility.binarytree import Tree


class Ray:
    __dir = []
    __dim = 0
    __start = []

    # путь луча

    def __init__(self, start: list, direction: list):
        if len(direction) == len(start):
            if not all(isinstance(i, float or int) and isinstance(j, float or int) for i, j in zip(start, direction)):
                raise AttributeError(
                    """Some element in %s or %s is not a float number..""" % (str(start), str(direction)))

            self.__dir = direction.copy()
            norm_val = np.linalg.norm(self.dir)
            if abs(norm_val - 1.0) > np.finfo(float).eps:
                self.__dir = np.dot(1 / norm_val, self.dir)
            self.__dim = len(direction)
            self.__start = start.copy()
            self.__path_of_ray = []
        else:
            raise AttributeError("""Iterables objects have different length. 
        len(start): %d,
        len(direction): %d""" % (len(start), len(direction)))

    # getter and setter====================================================================

    @property
    def dim(self):
        return self.__dim

    @property
    def dir(self) -> list:
        return self.__dir.copy()

    @property
    def start(self) -> list:
        return self.__start.copy()

    # @dir.setter
    # def set_dir(self, value):
    #     if len(value) == self.__dim:
    #         if all(isinstance(i, float or int) for i in value):
    #             self.__dir = value.copy()
    #         else:
    #             raise AttributeError("Some element in %s is not a digit" % (value.__name__))
    #     else:
    #         raise AttributeError("""Dimension of iterable object and ray are different.
    #         len(%s): %d,
    #         ray dimension: %d""" % (value.__name__, len(value), self.__dim))

    # @start.setter
    # def set_start(self, value):
    #     if len(value) == self.__dim:
    #         self.__start = value.copy()
    #     else:
    #         raise AttributeError("""Dimension of iterable object and ray are different.
    #             len(%s): %d,
    #             ray dimension: %d""" % (value.__name__, len(value), self.__dim))

    # methods of object ray====================================================================

    def __str__(self):
        return "ray:{ start: %s, direction: %s}" % (self.__start.__str__(), self.__dir.__str__())

    def __append_point_to_path(self, way_points_of_ray: list, point: list):
        if len(point) == 0:
            raise AttributeError("Zero dimensional point")
        if len(way_points_of_ray) != 0 and (len(point) != len(way_points_of_ray) or self.dim != len(point)):
            raise AttributeError(
                "Iterables objects(point) have different length with ray or way_points_of_ray. len(way_points_of_ray): %d, len(point): %d, ray(%d)" % (
                    len(way_points_of_ray), len(point), self.dim))
        if len(way_points_of_ray) == 0:
            for i in range(self.dim):
                way_points_of_ray.append([])
            for j in range(self.__dim):
                way_points_of_ray[j].append(self.start[j])
        for j in range(self.__dim):
            way_points_of_ray[j].append(point[j])

    def calc_point_of_ray(self, t: float):
        if not t > 10 * np.finfo(float).eps:
            return
        point = []
        for i in range(self.__dim):
            point.append(self.__start[i] + self.__dir[i] * t)
        return point

    def _reflect(self, surface: Surface):
        if self.__dim != surface.dim:
            raise AttributeError("Different dimension of ray(%d) and of surface(%d)" % (self.__dim, surface.dim))
        # ШАГ-1 ищем точку
        point = surface.find_nearest_point_intersection(self)
        if point == None:
            return
        # ШАГ-2 ищем вектор нормали к поверхности
        nrm = surface.norm_vec(point)
        # проверяем на на нужное направление нормального вектора
        # e__1 = np.dot(-1.0, self.dir)
        # if (np.dot(nrm, e__1) < 0):
        #     nrm = np.dot(-1.0, nrm)
        # ШАГ-3 отражаем луч
        e_n = 2 * np.dot(self.dir, nrm)
        e = np.subtract(self.dir, np.dot(e_n, nrm))
        e = np.dot(1 / np.linalg.norm(e), e)
        # print("surf" + str(surface))
        # print("nrm" + str(nrm))
        # print("e" + str(e))
        return Ray(point, list(e))

    def _refract(self, surface: Surface):
        if self.__dim != surface.dim:
            raise AttributeError("Different dimension of ray(%d) and of surface(%d)" % (self.__dim, surface.dim))
        point = surface.find_nearest_point_intersection(self)

        if point == None:
            return

        # ШАГ-2 ищем вектор нормали к поверхности
        nrm = None
        # если точки пересечения две найдем два вектора нормали, а если одна то одну
        nrm = surface.norm_vec(point)
        # проверяем на на нужное направление нормального вектора
        e__1 = np.dot(-1.0, self.dir)
        if (np.dot(nrm, e__1) < 0):
            nrm = np.dot(-1.0, nrm)
        # ШАГ-3 преломляем луч
        n1, n2 = surface.get_refractive_indexes(self.start)
        # calc the formula of refraction
        v1 = np.dot(n1, self.dir)
        v1n = np.dot(v1, nrm)
        # print("n1,n2 = %d,%d" %(n1, n2))
        # print("nrm = %s" %(str(nrm)))
        # print("v1 = %s" %(str(v1)))
        # print("v1n = %s" %(str(v1n)))
        expression = 1 + (n2 ** 2 - n1 ** 2) / (v1n ** 2)
        # print('expression' + str(expression))
        if expression < 0:
            return self._reflect(surface)
        k = (m.sqrt(expression) - 1) * v1n
        e = np.dot(1 / n2, v1 + np.dot(k, nrm))

        return Ray(point, list(e))

    def is_total_returnal_refruction(self, surface: Surface) -> bool:
        point = surface.find_nearest_point_intersection(self)
        if point == None:
            return False
        # ШАГ-2 ищем вектор нормали к поверхности
        nrm = None
        # если точки пересечения две найдем два вектора нормали, а если одна то одну
        nrm = surface.norm_vec(point)
        # проверяем на на нужное направление нормального вектора
        e__1 = np.dot(-1.0, self.dir)
        if (np.dot(nrm, e__1) < 0):
            nrm = np.dot(-1.0, nrm)
        # ШАГ-3 преломляем луч
        n1, n2 = surface.get_refractive_indexes(self.start)
        # calc the formula of refraction
        v1 = np.dot(n1, self.dir)
        v1n = np.dot(v1, nrm)
        # print("n1,n2 = %d,%d" %(n1, n2))
        # print("nrm = %s" %(str(nrm)))
        # print("v1 = %s" %(str(v1)))
        # print("v1n = %s" %(str(v1n)))
        expression = 1 + (n2 ** 2 - n1 ** 2) / (v1n ** 2)
        return expression < 0

    def _model_path(self, surfaces: list) -> list:
        way_point_of_ray = []
        while True:
            min_p = float(np.finfo(float).max)
            # index of nearest surface and intersection point
            index, i_point = -1, None
            # ищем ближайшую поверхность
            for i in range(len(surfaces)):
                point = None
                point = surfaces[i].find_nearest_point_intersection(self)
                if point == None:
                    continue
                print("point in m_p" + str(point))
                norm_val = np.linalg.norm(np.subtract(self.start, point))
                if norm_val < min_p:
                    min_p = norm_val
                    index = i
                    i_point = point
            if i_point == None:
                break
            new_ray = None
            # смотрим характер поверхности t - True пропускает через себя свет, f - False не пропускает
            print("Surf  " + str(surfaces[index]))
            if surfaces[index].type == Surface.types.REFLECTING:
                new_ray = self._reflect(surfaces[index])
            elif surfaces[index].type == Surface.types.REFRACTING:
                new_ray = self._refract(surfaces[index])

            if new_ray != None:
                self.__append_point_to_path(way_point_of_ray, new_ray.start)
                self.__dir = new_ray.dir
                self.__start = new_ray.start
                del new_ray
        return way_point_of_ray

    def path_ray(self, surfaces: list):
        if not all(isinstance(some, Surface) for some in surfaces):
            raise AttributeError(
                "Not all elements in surfaces is instance of class Surface %s" % (
                    str([type(some) for some in surfaces]))
            )
        self.__path_of_ray = self._model_path(surfaces)
        ans = self.__path_of_ray.copy()
        self.__append_point_to_path(ans, self.calc_point_of_ray(100_000))
        return ans

    def deep_modeling(self, surfaces: list, deep: int):
        if not all(isinstance(some, Surface) for some in surfaces):
            raise AttributeError(
                "Not all elements in surfaces is instance of class Surface %s" % (
                    str([type(some) for some in surfaces]))
            )
        if deep < 1:
            raise AttributeError(
                "Invalid deep value(%s)" % (
                    str(deep))
            )

        def fill_ray_tree(tree: Tree, surfaces: list, deep: int):
            ray = tree.value

            min_p = float(np.finfo(float).max)
            # index of nearest surface and intersection point
            index, i_point = -1, None
            # ищем ближайшую поверхность
            for i in range(len(surfaces)):
                point = None
                point = surfaces[i].find_nearest_point_intersection(ray)
                if point == None:
                    continue
                norm_val = np.linalg.norm(np.subtract(ray.start, point))
                if norm_val < min_p:
                    min_p = norm_val
                    index = i
                    i_point = point

            exit = False
            if i_point == None:
                tree.left = None
                tree.right = None
                exit = True
                i_point = ray.calc_point_of_ray(1)

            ray.__append_point_to_path(ray.__path_of_ray, i_point)
            if deep < 0:
                return

            if exit:
                return
            if Ray.is_total_returnal_refruction(ray, surfaces[index]):
                reflect_ray = Ray._reflect(ray, surfaces[index])
                tree.left = Tree(reflect_ray)
            else:
                refract_ray = Ray._refract(ray, surfaces[index])
                tree.right = Tree(refract_ray)
                reflect_ray = Ray._reflect(ray, surfaces[index])
                tree.left = Tree(reflect_ray)
            if tree.left is not None:
                fill_ray_tree(tree.left, surfaces, deep - 1)
            if tree.right is not None:
                fill_ray_tree(tree.right, surfaces, deep - 1)

        tree = Tree(self)
        fill_ray_tree(tree, surfaces, deep)
        return tree

    def draw_deep_ray_modeling(tree: Tree, axes, color='r'):
        count_of_rays = len(tree)
        for i, subtree in enumerate(tree):
            if isinstance(subtree.value, Ray):
                val = subtree.value
                # ,linewidth=count_of_rays - i
                line = pylab.Line2D(val.__path_of_ray[0], val.__path_of_ray[1], color=color,
                                    alpha=(count_of_rays - i) / count_of_rays)
                x_dir_of_text = [1, 0]
                y_dir_of_text = [0, 1]
                # для определения направления надписи относительно уже известного
                dir_of_ray = [coordinate[1] - coordinate[0] for coordinate in val.__path_of_ray]
                dir_of_ray_norm = np.linalg.norm(dir_of_ray)
                x_scalar_mul = np.dot(x_dir_of_text, dir_of_ray) / dir_of_ray_norm
                y_scalar_mul = np.dot(y_dir_of_text, dir_of_ray) / dir_of_ray_norm
                x_angle_of_rotation = int((np.arccos(x_scalar_mul) * 360 / 2 * np.pi))
                y_angle_of_rotation = int((np.arccos(y_scalar_mul) * 360 / 2 * np.pi))
                angle_of_rotation = None
                if y_angle_of_rotation <= 90:
                    angle_of_rotation = x_angle_of_rotation
                else:
                    angle_of_rotation = 360 - x_angle_of_rotation

                point_label = [np.average(coor) for coor in val.__path_of_ray]
                x_point_label = np.average(val.__path_of_ray[0])
                y_point_label = np.average(val.__path_of_ray[1])
                m = [[0, 1],
                     [-1, 0]]
                norm_dir_of_ray = np.linalg.norm(dir_of_ray)
                norm_to_ray = np.dot(np.dot(dir_of_ray, m), 1 / norm_dir_of_ray)


                point_label = np.add(point_label, norm_to_ray * 0.05 )
                axes.text(point_label[0], point_label[1], str(i + 1), va='center')

                line.set_label(str(i + 1))
                axes.add_line(line)

    def draw_ray(self, axes, way_points_of_ray: list, color="green"):
        if len(way_points_of_ray) == 2:
            axes.add_line(pylab.Line2D(way_points_of_ray[0], way_points_of_ray[1], color=color, marker=''))
        if len(way_points_of_ray) == 3:
            axes.plot(
                way_points_of_ray[0],
                way_points_of_ray[1],
                way_points_of_ray[2],
                label='LINE', color=color)
            axes.scatter(
                way_points_of_ray[0],
                way_points_of_ray[1],
                way_points_of_ray[2],
                c='b', marker='o')
