import pylab
import numpy as np

from view.matlab import polarization


def main():
    fig_num = 0
    sq2 = np.sqrt(2)

    vec_jonson = ((1, 0),
                  (0, 1),
                  (1 / sq2, complex(0, 1) / sq2),
                  (1 / sq2, complex(0, -1) / sq2),
                  (1 / sq2, complex(1, -1) / sq2),
                  (complex(1, -1) / sq2, 1 / sq2),
                  (complex(1, -1) / sq2, complex(1, -1) / sq2),
                  (complex(-1, 1) / sq2, complex(-1, 1) / sq2),
                  (complex(-1, 4) / sq2, complex(3, -1) ),
                  )
    str_title = ("vertically", "horizontly", "right circle", "left circle",
                 "unc", "unc")

    for i in range(len(vec_jonson)):
        pylab.figure(i)
        polarization.draw_polar_ellipse(vec_jonson[i], 100)
        pylab.grid()
    pylab.show()


if __name__ == '__main__':
    main()
