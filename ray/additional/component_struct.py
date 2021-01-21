"""
Component struct of RaysPool class.
It define inner structure of data for one ray at pool.
"""
from enum import IntEnum


class ComponInterface(IntEnum):
    pass


class Compon2D(ComponInterface):
    """
        Components of 2 dimension RAY
    """

    E_OFFSET = 0
    R_OFFSET = 2
    T0_OFFSET = 4
    T1_OFFSET = 5
    L_OFFSET = 6
    Jo_OFFSET = 7
    # For future code
    # LAM_OFFSET.value = 6
    # W_OFFSET.value = 7
    RAY_OFFSET = 9
    DIM = 2


class Compon3D(ComponInterface):
    """
        Components of  3 dimension  RAY
    """
    E_OFFSET = 0
    R_OFFSET = 3
    T0_OFFSET = 6
    T1_OFFSET = 7
    L_OFFSET = 8
    Jo_OFFSET = 9
    # For future code
    # LAM_OFFSET.value = 8
    # W_OFFSET.value = 9
    RAY_OFFSET = 11
    DIM = 3


def get_next_offset(compon_class, value_offset):
    """return next offset value.
    If it last value return it"""
    next_offset = None
    for i, val in enumerate(compon_class):
        if val > value_offset:
            next_offset = val
            break
        elif i == len(compon_class) - 1:
            next_offset = val
    return next_offset
