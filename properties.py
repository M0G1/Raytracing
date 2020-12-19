import os

EPS_D = 1e-15


class property:
    __APPLICATION_LOCATION = os.getcwd()

    @classmethod
    def get_ap_locaion(cls):
        return cls.__APPLICATION_LOCATION