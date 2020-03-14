from ray.rays_pool import *
from utility.generators import Generator
import binarytree as btr


def ray_pool_test():
    rays_arr = [i for i in range(0, 24)]

    ra = RaysPool(rays_arr)
    print(ra)
    ra.append_rays([i for i in range(2, 10)])
    print(ra)
    ra.erase_ray(2)
    print(ra)


def generator_test():
    print(type(np.pi))
    angles = [np.pi, np.pi, 0]
    shifts = [2, 1, 0]
    mat = Generator.rot_shift_mat(angles, shifts)
    print(mat)
    vector3D = [1, 1, 0]
    print("vector = " + str(vector3D))
    vector3D.append(0)
    print("new vector " + str(np.dot(mat, vector3D)))


def binary_tree_test():
    btr.tree()
    tree = btr.Node()


if __name__ == '__main__':
    # file = open("pic.txt")
    # print(file.readlines())
    print(Compon3D.T1_OFFSET == 7)
    print(Compon2D.T1_OFFSET == 5)
    print()

    print(Compon3D.DIM == 3)
    print(Compon2D.DIM == 2)
    print()

    print(issubclass(Compon3D, IntEnum))
    print(issubclass(Compon3D, Compon_Interface))

# generator_test()
