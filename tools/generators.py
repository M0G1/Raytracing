import numpy as np
import ray.rays_pool as rays_pool
from ray.abstract_ray import ARay


class Generator:
    @staticmethod
    def rot_shift_mat(rot_coef: list, shift_coef: list):
        if len(rot_coef) != 3 or len(shift_coef) != 3:
            raise AttributeError(
                "Coefficients is in wrong dimension. " +
                "rot_coef(%d),shift_coef(%d)" % (len(rot_coef), len(shift_coef)))
        if not all((isinstance(i, float) or isinstance(i, int))
                   and (isinstance(j, float) or isinstance(j, int))
                   for i, j in zip(rot_coef, shift_coef)):
            raise TypeError("Some element in rot_coef or shift_coef is not float or int")

        cos_r_c = [np.cos(arg) for arg in rot_coef]
        sin_r_c = [np.sin(arg) for arg in rot_coef]

        rot_mat_x = [
            [1, 0, 0],
            [0, cos_r_c[0], -sin_r_c[0]],
            [0, sin_r_c[0], cos_r_c[0]]
        ]
        rot_mat_y = [
            [cos_r_c[1], 0, sin_r_c[1]],
            [0, 1, 0],
            [-sin_r_c[1], 0, cos_r_c[1]]
        ]
        rot_mat_z = [
            [cos_r_c[2], -sin_r_c[2], 0],
            [sin_r_c[2], cos_r_c[2], 0],
            [0, 0, 1]
        ]
        rot_mat = list(np.matmul(np.matmul(rot_mat_x, rot_mat_y), rot_mat_z))
        # for i, val in enumerate(shift_coef):
        #     rot_mat[i] = list(rot_mat[i])
        #     rot_mat[i].append(val)
        #     print(rot_mat[i])
        # rot_mat.append([0, 0, 0, 1])
        # return rot_mat

    @staticmethod
    def generate_rays_2d(point1: list, point2: list, intensity: float) -> rays_pool.RaysPool:
        if len(point1) != 2 or len(point2) != 2:
            raise AttributeError("Point dimension is not 2. point1: " + str(point1) + " point2: " + str(point2))
        if (not all(isinstance(coor, (float, int)) for coor in point1)) or \
                (not all(isinstance(coor, (float, int)) for coor in point2)):
            raise AttributeError("Lists of point1 or list of point2 not contained type float or int")
        if intensity < np.finfo(float).eps:
            raise AttributeError("Negative intensity (%f)".format(intensity))

        vec = np.subtract(point2, point1)
        norm = np.linalg.norm(vec)
        # нормировка вектора для вычисления начал координат лучей
        vec = list(np.divide(vec, norm))
        pre_count = norm * intensity
        count = int(pre_count)
        # для равномерного распеределения в середине
        vec_t0 = (pre_count - count) / 2
        step = (norm - 2 * vec_t0) / (count - 1)
        m_rot = [[0, 1],
                 [-1, 0]]
        vec_e = np.dot(m_rot, vec)
        e_norm = np.linalg.norm(vec_e)
        # нормировка вектора направления
        vec_e = list(np.divide(vec_e, e_norm))
        arr_ray_pool = []
        # создаем бассейн с размерностью лучей 2(плоскость, а не пространство)
        # оставляем место для ячеек, куда мы не можем положить информацию. Заполняем только  e и r
        remain_len = rays_pool.Compon2D.RAY_OFFSET - (2 * rays_pool.Compon2D.DIM.value + 2)
        empty_list = [None for i in range(remain_len)]
        for i in range(count):
            vec_r = ARay.calc_point_of_ray_(vec, point1, vec_t0 + i * step)
            arr_ray_pool.extend(vec_e)
            arr_ray_pool.extend(vec_r)
            arr_ray_pool.append(0)
            arr_ray_pool.append(-1)
            arr_ray_pool.extend(empty_list)

        return rays_pool.RaysPool(arr_ray_pool, rays_pool.Compon2D)
