from utility import help as h
import matplotlib.pyplot as plt

# ======main===========================================================================

file = open("input2.txt")
rays, surfaces = h.read_param_from_file(file, 3)
file.close()
print(rays.path_ray([]))

if isinstance(rays, list):
    for i in rays:
        print(str(i))
else:
    print(str(rays))

print(not isinstance(surfaces, list))
if not isinstance(surfaces, list):
    temp = [surfaces]
    surfaces = temp

for i in surfaces:
    print(str(i))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

# rays.draw_ray(ax, rays.path_ray([]))
# opengl
#
for s in surfaces:
    s.draw_surface(ax)

plt.show()
