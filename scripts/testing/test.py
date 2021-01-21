from ray.rays_pool import RaysPool
from ray.additional.component_struct import *
from ray.abstract_ray import ARay
from surfaces.plane import Plane
from tools.generators import Generator
from utility.binarytree import Tree


def ray_pool_test():
    rays_arr = [i for i in range(0, 24)]

    ra = RaysPool(rays_arr, Compon2D)
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


def fill_tree(tree, deep: int, arr: list):
    if deep < 0:
        return
    print(f"left - {arr[0]}, rigth is {arr[0] + 1}")

    tree.left = Tree(arr[0])
    tree.right = Tree(arr[0] + 1)
    arr[0] = arr[0] + 2

    fill_tree(tree.left, deep - 1, arr)
    fill_tree(tree.right, deep - 1, arr)
    return tree


def binary_tree_test():
    tree = fill_tree(Tree(0), 3, [1])
    for i, subtree in enumerate(tree):
        print(f"i={i}, and value is {subtree.value}")


def raypool_offset():
    # file = open("pic.txt")
    # print(file.readlines())
    print(Compon3D.T1_OFFSET == 7)
    print(Compon2D.T1_OFFSET == 5)
    print()

    print(Compon3D.DIM == 3)
    print(Compon2D.DIM == 2)
    print()

    print(issubclass(Compon3D, IntEnum))
    print(issubclass(Compon3D, ComponInterface))


def aray_typing_test():
    e = [1, 0, 0]
    r = [2.3, 12, 3]
    p = Plane([3, 0, 0], [1, 0, 0])

    args = ARay.reflect_(e, r, p)

    print(f"ray: \ne = {e},\nr = {r}")
    print(f"{p}")
    print(f"{args}")

def time_():
    import time

    data = [[], []]
    for compon in (Compon2D, Compon3D):
        for index, fu in enumerate((get_next_offset,)):
            for i in compon:
                start = time.time()
                val = fu(compon, i)
                end = time.time()
                data[index].append(end - start)
                print(f"time of work {index} func is {end - start} value - {int(val)} : {str(val)}")

    print(data[0], "\n", data[1])

def main():
    time_()

# binary_tree_test()


if __name__ == '__main__':
    main()

# generator_test()
