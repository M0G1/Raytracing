import pylab
import numpy as np
import matplotlib

from controllers import polarization


def main():
    fig_num = 0
    sq2 = np.sqrt(2)

    vec_jonson = ((1, 0),
                  (0, 1),
                  (1 / sq2, complex(0, 1) / sq2),
                  (1 / sq2, complex(0, -1) / sq2),
                  )
    str_title = ("vertically", "horizontly", "right circle", "left circle")

    for i in range(len(str_title)):
        pylab.figure(i)
        polarization.draw_polar_ellipse(vec_jonson[i])
        pylab.grid()
    pylab.show()


if __name__ == '__main__':
    main()
