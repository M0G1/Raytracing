import numpy as np


# ============================================CHECKING==================================================================

def is_2d_complex_vector(vec: (np.array, list, tuple), **kwargs):
    """
    Check on Jones vector(two dimensional vector with complex numbers)
    """
    if len(vec) != 2:
        return False
    if any([not isinstance(vec[i], (float, int, complex)) for i in range(2)]):
        return False
    return True


def is_stokes_vector(vec: (np.array, list, tuple), float_dtype=np.float64):
    """
    Check on Stokes vector (four dimensional vector with real numbers)
    """
    if len(vec) != 4:
        return False
    if any([not isinstance(vec[i], (float, int)) for i in range(4)]):
        return False
    if vec[0] ** 2 - np.dot(vec[1:], vec[1:]) < -2 * np.finfo(float_dtype).eps:
        return False
    return True


# ==================================TRANSFORM OF PARAMETERS POLARISATION================================================


def jones_vector_to_stokes(vec: (np.array, list, tuple), is_need_check=True):
    """
                /E_DX\
    Jones vec = \E_DY/
    'E_DX^*' mean complex conjugation
                 /1  0  0  1\    /E_DX E_DX^*\
                |1  0   0  -1|  |E_DX E_DY^* |
    Stokes =    |0  1   1   0|  |E_DX^* E_DY |
                \0  i  -i  0/   \E_DY E_DY^*/

    """
    if is_need_check:
        is_2d_complex_vector(vec)
    from_jones_to_stokes_transform = np.array([[1, 0, 0, 1],
                                               [1, 0, 0, -1],
                                               [0, 1, 1, 0],
                                               [0, 1j, -1j, 0]], dtype=np.complex128)

    e_dx, e_dx_c = vec[0], complex.conjugate(vec[0]) if isinstance(vec[0], complex) else vec[0]
    e_dy, e_dy_c = vec[1], complex.conjugate(vec[1]) if isinstance(vec[1], complex) else vec[1]
    some_arr = np.array([
        e_dx * e_dx_c,
        e_dx * e_dy_c,
        e_dx_c * e_dy,
        e_dy * e_dy_c
    ])
    return np.array(np.matmul(from_jones_to_stokes_transform, some_arr), dtype=np.float64)


def stokes_vector_to_jones(vec: (np.array, list, tuple), is_need_check=True):
    if is_need_check:
        is_stokes_vector(vec)
    from_stokes_to_jones_transform = np.array([[0.5, 0.5, 0., 0.],
                                               [0., 0., 0.5, - 0.5j],
                                               [-0., -0., 0.5, 0.5j],
                                               [0.5, -0.5, 0., 0.]], dtype=np.complex128)
    some_arr = np.matmul(from_stokes_to_jones_transform, vec)
    jones_vec = np.zeros(2, dtype=np.complex128)
    if abs(some_arr[0]) > np.finfo(np.complex128).eps:
        jones_vec[0] = np.sqrt(float(some_arr[0]))
        jones_vec[1] = some_arr[2] / jones_vec[0]
    elif abs(some_arr[3]) > np.finfo(np.complex128).eps:
        jones_vec[1] = np.sqrt(float(some_arr[3]))
        jones_vec[0] = some_arr[1] / jones_vec[1]
    else:
        print("Given vector is equal 4dim space zero" + str(vec))
    return jones_vec


# =====================================ELLIPSE POLARISATION PARAMETERS==================================================

def get_param_ellipse_polar_for_stokes(vec: (np.array, list, tuple), is_need_check=True, float_dtype=np.float64):
    """
        vec - Stokes vector (four dimensional vector with real numbers) double precision is default
        Stokes vector must have polarisation. The elements vec[1],vec[2],vec[3] must not equal zero.
        float_dtype - numpy type of float data ()
        Return alpha, Beta

        alpha - polarization ellipse azimuth.   -pi/2 <= alpha <= pi/2
        beta - angle of ellipticity.            -pi/4 <= beta <= pi/4

        sing of beta show direction of polarization.
        For positive beta - right polarisation.
        For negative - left polarisation.

        Еhe vector electric field strength rotates clockwise for an observer
        looking in the opposite direction of radiation propagation,
        then the polarization is called right elliptical, else left.
    """
    if not (float_dtype in (np.float32, np.float64, np.complex64, np.complex128)):
        float_dtype = np.float64
    if is_need_check:
        if not is_stokes_vector(vec):
            raise ValueError(f"Argument vec {vec} is not Stokes vector")
    if np.all(np.absolute(np.array(vec)) < np.finfo(float_dtype).eps):
        raise ValueError(f"All components of Vec {vec} equal 0")
    alpha = 0
    beta = 0
    # only A_Y component. vec[0] + vec[1] = 2*A_X
    if abs(vec[0] + vec[1]) > np.finfo(float_dtype).eps:
        # check arctan(INF)
        if abs(vec[1]) > np.finfo(float_dtype).eps:
            alpha = np.arctan(vec[2] / vec[1]) / 2
        else:
            alpha = (np.pi / 4) * (-1) ** (int(vec[2] < 0))
    else:
        alpha = np.pi / 2
    norm = np.linalg.norm(vec[1:])
    if norm > np.finfo(float_dtype).eps:
        beta = np.arcsin(vec[3] / norm) / 2
    else:
        raise ValueError(f"The light is not polarised. It Stokes vector {vec}")
    return alpha, beta


def get_param_ellipse_polar_for_jones(vec: (np.array, list, tuple), is_need_check=True, float_dtype=np.float64):
    """
        vec - Jones vector(two dimensional vector with complex numbers) double precision is default
        Return (alpha,Beta)

        alpha - polarization ellipse azimuth.   -pi/2 <= alpha <= pi/2
        beta - angle of ellipticity.            -pi/4 <= beta <= pi/4
        float_dtype - numpy type of float data ()

        sing of beta show direction of polarization.
        For positive beta - right polarisation.
        For negative - left polarisation.

        Еhe vector electric field strength rotates clockwise for an observer
        looking in the opposite direction of radiation propagation,
        then the polarization is called right elliptical, else left.
    """
    if not (float_dtype in (np.float32, np.float64, np.complex64, np.complex128)):
        float_dtype = np.float64
    if is_need_check:
        if not is_2d_complex_vector(vec):
            raise ValueError(f"Argument vec {vec} is not Jones vector")
    if np.all(np.absolute(np.array(vec)) < np.finfo(float_dtype).eps):
        raise ValueError(f"All components of Vec {vec} equal 0")

    xi: complex = complex(0, 0)
    alpha = 0
    if abs(vec[0]) > np.finfo(float_dtype).eps:
        xi: complex = vec[1] / vec[0]
    else:
        alpha = (np.pi / 2) * (-1) ** (int(xi.real < 0))

    abs_xi = np.absolute(xi)
    if abs_xi > np.finfo(float_dtype).eps:
        if np.abs(abs_xi - 1) > np.finfo(float_dtype).eps * 10:
            arg = 2 * xi.real / (1 - abs_xi ** 2)
            # print(arg)
            alpha = np.arctan(arg) / 2
        else:
            # component A_X equal zero
            # handle tg(+-1/0)=tg(+-inf)
            alpha = (np.pi / 4) * (-1) ** (int(xi.real < 0))

    beta = np.arcsin(2 * xi.imag / (1 + abs_xi ** 2)) / 2
    return alpha, beta


def get_param_ellipse_polar(vec: (np.array, list, tuple), float_dtype=np.float64):
    """
    vec - Stokes or Jones vector
    Stokes vector - four dimensional vector with real numbers
        Stokes vector must have polarisation. The elements vec[1],vec[2],vec[3] must not equal zero.
    Jones vector - two dimensional vector with complex numbers
    float_dtype - numpy type of float data ()

    return alpha beta

    alpha - polarization ellipse azimuth.   -pi/2 <= alpha <= pi/2
    beta - angle of ellipticity.            -pi/4 <= beta <= pi/4\

    sing of beta show direction of polarization.
    For positive beta - right polarisation.
    For negative - left polarisation.

    Еhe vector electric field strength rotates clockwise for an observer
    looking in the opposite direction of radiation propagation,
    then the polarization is called right elliptical, else left.
    """
    if is_2d_complex_vector(vec):
        return get_param_ellipse_polar_for_jones(vec, is_need_check=False, float_dtype=float_dtype)
    if not (float_dtype in (np.float32, np.float64, np.complex64, np.complex128)):
        float_dtype = np.float64
    if is_stokes_vector(vec, float_dtype=float_dtype):
        return get_param_ellipse_polar_for_stokes(vec, is_need_check=False, float_dtype=float_dtype)


# =======================================GETTING STR VIEW===============================================================

def get_str_view_jones(vec: (np.array, list, tuple), is_need_check=True, fp: int = 2) -> str:
    if is_need_check:
        if not is_2d_complex_vector(vec):
            return f"This is not Jones vector {vec}"
    return (f"Jones vector (%.{fp}f %.{fp}fj,%.{fp}f %.{fp}fj)") % \
           (complex(vec[0]).real, complex(vec[0]).imag,
            complex(vec[1]).real, complex(vec[1]).imag)


def get_str_view_stokes(vec: (np.array, list, tuple), is_need_check=True, fp: int = 2, float_dtype=np.float64) -> str:
    if is_need_check:
        if not is_stokes_vector(vec, float_dtype=float_dtype):
            return f"This is not Stokes vector {vec}"
    return (f"Stokes vector (%.{fp}f, %.{fp}f,%.{fp}f, %.{fp}f)") % (vec[0], vec[1], vec[2], vec[3])


def get_str_view_polar_vec(vec: (np.array, list, tuple), fp: int = 2, float_dtype=np.float64) -> str:
    """
    vec - Stokes or Jones vector
    Stokes vector - four dimensional vector with real numbers
        Stokes vector must have polarisation. The elements vec[1],vec[2],vec[3] must not equal zero.
    Jones vector - two dimensional vector with complex numbers
    float_dtype - numpy type of float data ()

    return str view of Jones vector or Stokes vector
    """
    if is_2d_complex_vector(vec):
        return get_str_view_jones(vec, is_need_check=False, fp=fp)
    if not (float_dtype in (np.float32, np.float64, np.complex64, np.complex128)):
        float_dtype = np.float64
    if is_stokes_vector(vec, float_dtype=float_dtype):
        return get_str_view_stokes(vec, is_need_check=False, fp=fp)
    return f"This is not Stokes or Jones vector {vec}"
