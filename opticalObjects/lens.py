class Lens:
    """
        RUS
        (x-x0)^2/a^2 + (y - y0)^2/b^2 + (z - z0)^2/c^2 = 1 - каноническое уравнение эллипса
        :argument ellipse_coefficients1, ellipse_coefficients2 - числа a,b,c из какнонического уравнения эллипса
        :argument center_distance - растояние между центрами элипса (x0,y0,z0) - центр эллипса
        :argument lens_center - точка лежащая на пересечении (главной оптической оси,
        и линии проведенной соединением пересечений эллипсов)
        :argument n1,n2 - оптические коэфициенты
        ENG
        (x-x0) ^ 2 / a ^ 2 + (y - y0) ^ 2 / b ^ 2 + (z - z0) ^ 2 / c ^ 2 = 1 - canonical equation of the ellipse
        :argument ellipse_coefficients1, ellipse_coefficients2 - numbers a, b, c from the canonical ellipse equation
        :argument center_distance - the distance between the centers of the ellipse (x0, y0, z0) - the center of the ellipse
        :argument lens_center - the point lying at the intersection (of the main optical axis,
         and lines drawn by connecting intersections of ellipses)
        :argument n1, n2 - optical coefficients
    """
    def __create_limited_surfaces(self):
        pass

    def __init__(self, ellipse_coefficients1: list, ellipse_coefficients2: list,
                 centers_distance: [float, int], lens_center: list, n1: float, n2: float):
        ell_coef1 = ellipse_coefficients1
        ell_coef2 = ellipse_coefficients2
        if len(ell_coef1) != len(ell_coef2) != len(lens_center):
            raise AttributeError("Ellipse coefficients(1: %d, 2: %d) and lens center(%d) have different length" %
                                 (len(ell_coef1), len(ell_coef2), len(lens_center)))
        if centers_distance <= 0:
            raise AttributeError("Invalid centers distance: %s" % (str(centers_distance)))
        if n1 < 1 or n2 < 1:
            raise AttributeError("Optical coefficients can not be less 1.n1(%s),n2(%s)" % (str(n1), str(n2)))
        self.__ell_coef1 = ell_coef1
        self.__ell_coef2 = ell_coef2
        self.__center_dist = centers_distance
        self.__lens_center = lens_center
        self.__n1 = n1
        self.__n2 = n2
        self.__create_limited_surfaces()

