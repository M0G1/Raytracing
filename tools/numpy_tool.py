"""
Include some tool useful, when u work with numpy
reshaping
type check
"""
import numpy as np


# =================================================== reshaping ========================================================


def reshape_arrays_into_one(*args):
    """
    Arrays must have the same length
    reshape given arrays
    x = [x0,x1,...,xn]
    y = [y0,y1,...,yn]
    ...
    z = [z0,z1,...,zn]
    into
    ans = [x0,y0,...,z0,x1,y1,...,z1,...,xn,yn,zn]


    return numpy.array
    """
    narray = np.array(args)
    return narray.ravel(order='F')


def reshape_array_into_many(arr, row_count, column_count):
    """
    Better to use numpy.reshape(). This method just recall it.
    reshape given array
    arr = [x0,y0,...,z0,x1,y1,...,z1,...,xn,yn,zn]
    into

    x = [x0,x1,...,xn]
    y = [y0,y1,...,yn]
    ...
    z = [z0,z1,...,zn]

    return numpy.array
    """
    return np.reshape(arr, (row_count, column_count), order='F')


# =================================================== type check =======================================================

NUMPY_INT_TYPES = (np.int8, np.int16, np.int32, np.int64)
NUMPY_UINT_TYPES = (np.uint8, np.uint16, np.uint32, np.uint64)
NUMPY_FLOAT_TYPES = (np.float32, np.float64)
NUMPY_COMPLEX_TYPES = (np.complex64, np.complex128)

NUMPU_FLOAT_POINT_TYPES = (*NUMPY_FLOAT_TYPES, *NUMPY_COMPLEX_TYPES)
# can be cast to REAL or COMPLEX types
NUMPY_REAL_NUM_TYPE = (*NUMPY_INT_TYPES, *NUMPY_UINT_TYPES, *NUMPY_FLOAT_TYPES)
NUMPY_COMPLEX_NUM_TYPE = (*NUMPY_REAL_NUM_TYPE, *NUMPY_COMPLEX_TYPES)


def is_numpy_real_num_type(np_arr: np.ndarray) -> bool:
    """
    Numbers consider real if it can be cast to some real numpy type without losing the information.
    All transition from complex to real is prohibited!
    """
    return np_arr.dtype in NUMPY_REAL_NUM_TYPE


def is_numpy_complex_num_type(np_arr: np.ndarray) -> bool:
    """Numbers consider real if it can be cast to some complex numpy type."""
    return np_arr.dtype in NUMPY_COMPLEX_NUM_TYPE


def is_float_point_type(dtype: type) -> bool:
    """check on real or complex type number"""
    return dtype in NUMPU_FLOAT_POINT_TYPES
