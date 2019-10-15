from ray.rays_pool import *

rays_arr = [i for i in range(0, 24)]

ra = RaysPool(rays_arr)
print(ra)
ra.append_rays([i for i in range(2, 10)])
print(ra)
ra.erase_ray(2)
print(ra)

