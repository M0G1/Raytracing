import numpy as np
from typing import List, Union

from ray.rays_pool import RaysPool
from surfaces.surface import Surface
from ray.additional.component_struct import *

class RayPoolVec(RaysPool):
    """
    Form of reorganise of code to decrease the count of code row at class RaysPoll
    There is having a vector methods for access to few beam at the same time.
    """
    pass