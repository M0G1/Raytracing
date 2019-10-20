import numpy as np


class Generator:
    @classmethod
    def rot_shift_mat(cls, rot_coef: list, shift_coef: list):
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
