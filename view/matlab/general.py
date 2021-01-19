"""
Some general methods for working with matlplotlib
"""
import numpy as np

def focus_on_without_cutting(xlim: (np.array, list, tuple), ylim: (np.array, list, tuple),
                             x: (np.array, list, tuple), y: (np.array, list, tuple), indent: float):
    """
    xlim, ylim - default area
    x,y - float point data
    indent - indent borders from data
    Return xlim and ylim, what includes the area that you specified in coordinates, while expanding it if data leaves it
    """
    if len(xlim) != len(ylim) != 2:
        raise ValueError(f"Limits must have length equals xlim {xlim}, ylim {ylim}")
    indents = (-indent, +indent)
    x_min = min(xlim[0], np.min(x))
    x_max = max(xlim[1], np.max(x))
    y_min = min(ylim[0], np.min(y))
    y_max = max(ylim[1], np.max(y))

    return np.add((x_min, x_max), indents), np.add((y_min, y_max), indents)