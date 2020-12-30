import pylab
import numpy as np

from view.matlab import polarization
from controllers.polarization import jones_vector_to_stokes, stokes_vector_to_jones, \
    get_str_view_stokes, get_str_view_jones


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
                  (complex(-1, 4) / sq2, complex(3, -1)),
                  )
    str_title = ("vertically", "horizontly", "right circle", "left circle",
                 "unc", "unc")

    for i in range(len(vec_jonson)):
        stokes = jones_vector_to_stokes(vec_jonson[i])
        jones = stokes_vector_to_jones(stokes)
        str_stokes = get_str_view_stokes(stokes)
        str_jones = get_str_view_jones(vec_jonson[i])
        str_jones_2 = get_str_view_jones(jones)
        print("from", str_jones, "to", str_stokes)
        print("from", str_stokes, "to", str_jones_2,"\n")
        pylab.figure(3 * i)
        polarization.draw_polar_ellipse(vec_jonson[i], 100)
        pylab.grid()
        pylab.figure(3 * i + 1)
        polarization.draw_polar_ellipse(stokes, 100)
        pylab.grid()
        pylab.figure(3 * i + 2)
        polarization.draw_polar_ellipse(jones, 100)
        pylab.grid()
        pylab.show()


if __name__ == '__main__':
    main()
