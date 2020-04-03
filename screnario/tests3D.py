import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def ellipse(axes, abc: list, center: list = [0, 0, 0], color='b', alpha=0.5):
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)

    x = np.subtract(abc[0] * np.outer(np.cos(u), np.sin(v)), -center[0])
    y = np.subtract(abc[1] * np.outer(np.sin(u), np.sin(v)), -center[1])
    z = np.subtract(abc[2] * np.outer(np.ones(np.size(u)), np.cos(v)), -center[2])

    axes.plot_surface(x, y, z, rstride=4, cstride=4, color=color, alpha=alpha)


def line(axes, x, y, z, color='b'):
    ax.plot(x1, x1, x1, label='LINE', color=color)


def points(axes, x, y, z, color='b', marker='o'):
    axes.scatter(p, p, p, c='b', marker='o')


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
x1 = np.linspace(0, 2, 2)
p = [3, 0]

points(ax, p, p, p)
line(ax, x1, x1, x1, color='green')
ellipse(ax, [1, 2, 1], [1, 1, 1])
ellipse(ax, [0.1, 0.2, 0.1], [0, 0, 0])

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
plt.show()
