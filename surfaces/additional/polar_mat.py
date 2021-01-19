"""
This module additive the surface class.
It additive working with polarization matrix.
"""
import numpy as np
from typing import List, Tuple, Callable, Dict

import tools.numpy_tool

_LEFT: str = "left"
_RIGHT: str = "right"


class PolarMat():
    """
    class PolarMat - Polarisation matrix
    It responsibility is transform polarisation of light
    with helping of matrix multiplication on vector Jones or parameters of Stokes

    It can contains some inner variable for returned transform matrix(optional)
    """

    def __init__(self, trans_mat: (List[float or int or complex], np.ndarray) = np.identity(2, dtype=float)):
        """
        trans_mat - transform polarisation of light matrix
            For Jones vector - 2 x 2 matrix with complex values (Jones matrix)
            For Stokes parameters - 4 x 4 float (Muller matrix)
            Identity matrix Jones is default
        """
        res1, res2 = PolarMat._check_and_return_val(trans_mat)
        self.trans_mat: np.ndarray = res1
        # Boolean maker. If True - it is a Jones matrix. If False is a Muller matrix
        self.is_jones: bool = res2
        self.depend_param: Dict[str, List[Tuple[str]]] = {_LEFT: list(), _RIGHT: list()}
        self.addit_mat_func: Dict[str, List[Callable]] = {_LEFT: list(), _RIGHT: list()}

    # =========================================== property and inner state =============================================

    @property
    def dependence_param(self):
        return self.depend_param

    @property
    def additional_mat_func(self):
        return self.addit_mat_func

    @property
    def transform_mat(self):
        return self.trans_mat

    @transform_mat.setter
    def transform_mat(self, val: (List[float or int or complex], np.ndarray)):
        res1, res2 = PolarMat._check_and_return_val(val)
        self.trans_mat = res1
        self.is_jones = res2

    def is_it_jones_matrix(self):
        return self.is_jones

    # =========================================== accessor methods =============================================

    def add_dependence_from_param(self, param: Tuple[str], side: str, func: Callable):
        """
        Add function, returned needed matrix(for Jones any 2 x 2 matrix with complex number,
        for Muller any 4 x 4 matrix with real number). It doesn't check.
        When call "get_polar_mat". U need give named params and they will redirect to  given function.
        Param can be empty to change matrix, but better set "transform_mat" parameter.

        param - tuple of str, name of named parameters within given function.
            It must be uniq or to have the same mean to work correct.
        side - "left" of "right". It definite the side of multiplication of this matrix.
        func - function only with named parameters.
        """
        if side not in (_LEFT, _RIGHT):
            raise ValueError(f"Side must be '{_LEFT}' or '{_RIGHT}' values. Given value:{side}")
        self.depend_param[side].append(param)
        self.addit_mat_func[side].append(func)

    def remove_dependence_from_param(self, param: Tuple[str], side: str, func: Callable):
        """
        Remove function, returned needed matrix(for Jones any 2 x 2 matrix with complex number,
        for Muller any 4 x 4 matrix with real number). It doesn't check.

        Reverse operation to add_dependence_from_param.

        param - tuple of str, name of named parameters within given function.
            It must be uniq or to have the same mean to work correct.
        side - "left" of "right". It definite the side of multiplication of this matrix.
        func - function only with named parameters.
        """
        if side not in (_LEFT, _RIGHT):
            raise ValueError(f"Side must be '{_LEFT}' or '{_RIGHT}' values. Given value:{side}")
        self.depend_param[side].remove(param)
        self.addit_mat_func[side].remove(func)

    def get_polar_mat(self, **kwargs):
        """
        Returning the polar transform matrix for Jones or Stokes vectors.
        If added dependence from param it will redirect to needed function.
        Their result will matrix multiply on inner matrix on left from first added to last.
        M_n * M_n-1 * ... * M_1 * M_inner
        """

        def search_kwargs(param: Tuple[str], **kwargs_) -> dict:
            """
            return dictionary only with params where names matches with "param" values
            Optimization. It it doesn't have a normal realization, please will write it.
            """
            return kwargs_

        result = self.trans_mat.copy()
        n = len(self.depend_param[_LEFT])
        for i in range(n).__reversed__():
            needed_kwargs = search_kwargs(self.depend_param[_LEFT][i], **kwargs)
            new_mat = self.addit_mat_func[_LEFT][i](**needed_kwargs)
            result = np.dot(new_mat, result)

        n = len(self.depend_param[_RIGHT])
        for i in range(n).__reversed__():
            needed_kwargs = search_kwargs(self.depend_param[_RIGHT][i], **kwargs)
            new_mat = self.addit_mat_func[_RIGHT][i](**needed_kwargs)
            result = np.dot(result, new_mat)
        return result

    # =========================================== static methods =======================================================

    @staticmethod
    def _check_and_return_val(trans_mat) -> (np.ndarray, bool):
        """
        Check the trans_mat (transform polarisation of light matrix)
            It must be 2 x 2 matrix with complex values (Jones matrix) or 4 x 4 float (Muller matrix)
        And return trans_mat and boolean value, what mean is jones matrix or not.
        """
        is_jones = PolarMat.is_matrix_jones(trans_mat)
        if not is_jones or not PolarMat.is_matrix_muller(trans_mat):
            raise ValueError(f"trans_mat must be a Jones or Muller matrix!\n{trans_mat}\n" +
                             "Jones matrix is a 2 x 2 complex matrix." +
                             "Muller matrix is a 4 x 4 real matrix.")
        return np.asarray(trans_mat), is_jones

    @staticmethod
    def is_matrix_jones(trans_mat: (List[float or int or complex], np.ndarray)):
        trans_mat = np.ndarray(trans_mat)
        if trans_mat.shape != (2, 2):
            return False
        elif not tools.numpy_tool.is_numpy_complex_num_type(trans_mat):
            return False
        else:
            return True

    @staticmethod
    def is_matrix_muller(trans_mat: (List[float or int or complex], np.ndarray)):
        trans_mat = np.ndarray(trans_mat)
        if trans_mat.shape != (4, 4):
            return False
        elif not tools.numpy_tool.is_numpy_real_num_type(trans_mat):
            return False
        else:
            return True

    @staticmethod
    def from_jones_to_muller_matrix(trans_mat: (List[float or int or complex], np.ndarray)):
        """
        It doesn't have a realization
        Transform Jones matrix to Muller
        """
        pass

    @staticmethod
    def from_muller_to_jones_matrix(trans_mat: (List[float or int or complex], np.ndarray)):
        """
        It doesn't have a realization
        Transform Muller matrix to Jones
        """
        pass
