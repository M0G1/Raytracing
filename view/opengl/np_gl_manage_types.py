import numpy as np
from OpenGL import GL


class NP_GL_Types:
    """Class for managing the np and gl data types"""

    def __init__(self, digit_float_capacity: int = 32, digit_int_capacity: int = 64, is_integer_unsigned: bool = True,
                 min_int_val=None, max_int_val=None):
        """
        digit_float_capacity must have value 16,32 or 64
        digit_int_capacity must have value 8,16,32
        Created to manipulate integer types and storage np and gl types
        """

        self.npf = None
        self.glf = None
        self.sizeof_f = 4

        self._npi = None
        self._gli = None
        self.sizeof_i = None
        self.is_integer_unsigned = is_integer_unsigned
        self._max_bites_integer = digit_int_capacity
        self._is_set_integer_types = False

        self._set_float_types(digit_float_capacity)
        min_int_val, max_int_val = NP_GL_Types._handle_int_args(digit_int_capacity, is_integer_unsigned,
                                                                min_int_val, max_int_val)
        self.set_integer_types(max_int_val, min_int_val)

    def _set_float_types(self, digit_float_capacity: int):
        if digit_float_capacity == 32:
            self.npf = np.float32
            self.glf = GL.GL_FLOAT
            self.sizeof_f = 4
        elif digit_float_capacity == 64:
            self.npf = np.float_
            self.glf = GL.GL_DOUBLE
            self.sizeof_f = 8
        elif digit_float_capacity == 16:
            self.npf = np.float16
            self.glf = GL.GL_HALF_FLOAT
            self.sizeof_f = 16

    @staticmethod
    def _handle_int_args(digit_int_capacity: int, is_integer_unsigned: bool, min_int_val, max_int_val):
        if min_int_val is None or max_int_val is None:
            if min_int_val is None and max_int_val is None:
                min_int_val, max_int_val = NP_GL_Types._transform_digit_int_capacity_into_range(
                    digit_int_capacity, is_integer_unsigned)
                # this works. don't pull out the return statement
            elif min_int_val is None:
                ans = NP_GL_Types._transform_digit_int_capacity_into_range(
                    digit_int_capacity, is_integer_unsigned)
                min_int_val = ans[0]
            else:
                ans = NP_GL_Types._transform_digit_int_capacity_into_range(
                    digit_int_capacity, is_integer_unsigned)
                max_int_val = ans[1]

        return min_int_val, max_int_val

    @staticmethod
    def _transform_digit_int_capacity_into_range(digit_int_capacity: int, is_integer_unsigned):
        # don't transform lover bound because it will work correctly only with upper bound
        if is_integer_unsigned:
            max_int_val = (2 ** digit_int_capacity) - 1
        else:
            max_int_val = (2 ** (digit_int_capacity - 1)) - 1
        return 0, max_int_val

    def _set_unsigned_integer_types(self, max_int_val: int):
        """sets the desired types depending on the maximum integer value """
        MAX_UINT64 = 18446744073709551615
        MAX_UINT32 = 4294967295
        # key is the max unsigned integer value
        NP_UINT_TYPES = {
            255: np.uint8,
            65535: np.uint16,
            MAX_UINT32: np.uint32,
            MAX_UINT64: np.uint64
        }

        GL_UINT_TYPES = {
            255: GL.GL_UNSIGNED_BYTE,
            65535: GL.GL_UNSIGNED_SHORT,
            MAX_UINT32: GL.GL_UNSIGNED_INT,
            MAX_UINT64: GL.GL_UNSIGNED_INT64
        }
        for pow_, key in enumerate(NP_UINT_TYPES):
            if max_int_val <= key:
                self._npi = NP_UINT_TYPES[key]
                self._gli = GL_UINT_TYPES[key]
                self.sizeof_i = 2 ** pow_
                break
        else:
            self._npi = NP_UINT_TYPES[MAX_UINT64][0]
            self._gli = GL_UINT_TYPES[MAX_UINT64][0]
            self.sizeof_i = 8
        # if system 32bit and we need 64. Sorry
        if self._npi == NP_UINT_TYPES[MAX_UINT64] and self._max_bites_integer == 32:
            self._npi = NP_UINT_TYPES[MAX_UINT32][0]
            self._gli = GL_UINT_TYPES[MAX_UINT32][0]
            self.sizeof_i = 4

    def _set_singned_integer_types(self, max_int_val: int, min_int_val: int):
        INT32_RANGE = (-2147483648, 2147483647)
        NP_INT_TYPES = {
            (-128, 127): np.int8,
            (-32768, 32767): np.int16,
            INT32_RANGE: np.int32
            # ,
            # (-9223372036854775808, 9223372036854775807): np.int64
        }
        GL_INT_TYPES = {
            (-128, 127): GL.GL_BYTE,
            (-32768, 32767): GL.GL_SHORT,
            INT32_RANGE: GL.GL_INT
            # ,
            # (-9223372036854775808, 9223372036854775807): GL.GL_ NOT FOUND
        }
        for pow_, key in enumerate(NP_INT_TYPES):
            if min_int_val <= key[0] and max_int_val <= key[1]:
                self._npi = NP_INT_TYPES[key]
                self._gli = GL_INT_TYPES[key]
                self.sizeof_i = 2 ** pow_
                break
        else:
            self._npi = NP_INT_TYPES[INT32_RANGE]
            self._gli = GL_INT_TYPES[INT32_RANGE]
            self.sizeof_i = 4

    def set_integer_types(self, max_int_val: int, min_int_val: int = 0):
        if min_int_val == 0 or min_int_val is None:
            self._set_unsigned_integer_types(max_int_val)
        else:
            self._set_singned_integer_types(max_int_val, min_int_val)
        self._is_set_integer_types = True

    @property
    def npi(self):
        return self._npi

    @property
    def gli(self):
        return self._gli
