import numpy as np
import pickle
import pathlib


class Sphere_Ellipse_data_2Dview:
    """
        Class work with loading and uploading data for sphere or ellipse to view.
        partition = segment
    """
    """
        structure of sefvise data - dict(key - string info about section of service data :
        value - another structure describing this section
    """
    __service_data = None
    __PARTITION_SEGMENT = "existing partition"
    __SERVICE_INFO_LOCATE = pathlib.Path("sphereEllipseSerialization")

    @classmethod
    def __get_service_data(cls) -> dict:
        try:
            with open(file=(cls.__SERVICE_INFO_LOCATE / 'service_information.txt'),
                      mode="rb") as file:
                return pickle.load(file=file)
        except TypeError:
            print("TypeError.")
        except EOFError:
            print("EOFError. Data is may be not initialized")

    @classmethod
    def __pickle_service_data(cls):
        with open(file=(cls.__SERVICE_INFO_LOCATE / 'service_information.txt'), mode="wb") as file:
            pickle.dump(obj=cls.__service_data, protocol=3, file=file)

    # Hope what it will initialize the __service_data
    def __new__(cls, *args, **kwargs):
        super().__new__(cls)

    @classmethod
    def __init_service_data(cls):
        if cls.__service_data is None or not isinstance(cls.__service_data, dict):
            cls.__service_data = Sphere_Ellipse_data_2Dview.__get_service_data()

    @classmethod
    def __load_sphere_partition_from_file(cls, fileName):
        with open(file=fileName, mode="rb") as data_file:
            return pickle.load(data_file)

    # D:\Projects\Python\rayTracingOOPwithGIT\view\sphereEllipseSerialization\service_information.txt
    # view/sphereEllipseSerialization/service_information.txt

    @classmethod
    def __pickle_sphere_partition_to_file(cls, partit: tuple, step: float):
        # try to open service data
        cls.__init_service_data()

        file_name = cls.__SERVICE_INFO_LOCATE / ("partit" + str(step))

        # load to file
        with open(file=file_name, mode="wb") as data_file:
            pickle.dump(partit, file=data_file, protocol=3)

        # save information
        # create if not exist service data
        if cls.__service_data is None:
            cls.__service_data = dict()

        # create if not exist segment of partitions service data
        partitions = cls.__service_data.setdefault(cls.__PARTITION_SEGMENT, dict())

        # save partition
        partitions.setdefault(step, file_name)

        # update service data
        cls.__pickle_service_data()

    @classmethod
    def __is_step_exist(cls, step: float) -> str:
        """
        :return: path to file if that partition with step is exist
        """
        # try to open service data
        cls.__init_service_data()

        # getting a dict with service info
        if cls.__service_data is None or not isinstance(cls.__service_data, dict):
            return ""

        # getting a dict with partitions
        existing_partit = cls.__service_data.get(cls.__PARTITION_SEGMENT)

        if existing_partit is None or not isinstance(existing_partit, dict):
            return ""

        # return filename
        ans = existing_partit.get(step)
        if ans is None or not isinstance(ans, str):
            return ""
        return ans

    @classmethod
    def __get_partit(cls, step: float, is_ellipse: bool = False, ab: iter = (1, 1),
                     is_shift=False, center: iter = (0, 0)
                     ) -> iter:
        file_name = cls.__is_step_exist(step)
        partit = None
        # create/load fourth part partition of sphere
        if file_name is not "":
            partit = cls.__load_sphere_partition_from_file(file_name)
        else:
            spaced_values = np.arange(start=0, stop=np.pi / 2 + step, step=step)
            partit = (np.cos(spaced_values), np.sin(spaced_values))
            cls.__pickle_sphere_partition_to_file(partit, step)

        if is_ellipse:
            partit = [np.multiply(ab[i], partit[i]) for i in range(2)]

        # create others part of sphere/ellipse
        # # rot on 90 degree anti clock wise
        # rot_mat = [
        #     [0, -1],
        #     [1, 0]]
        # second_fourth1 = np.matmul(rot_mat, partit)
        # third_fourth1 = np.matmul(rot_mat, second_fourth1)
        # fourth_fourth1 = np.matmul(rot_mat, third_fourth1)

        # reverse
        reversed_x = partit[0][::-1]
        reversed_y = partit[1][::-1]

        second_fourth = (np.multiply(-1, reversed_x), reversed_y)
        third_fourth = (np.multiply(-1, partit[0]), np.multiply(-1, partit[1]))
        fourth_fourth = (reversed_x, np.multiply(-1, reversed_y))

        ellipse = (partit, second_fourth, third_fourth, fourth_fourth)
        # print(ellipse)

        to_draw = [[], []]
        for i in range(2):
            for j in range(4):
                to_draw[i].extend(ellipse[j][i])

        if is_shift:
            to_draw = [np.add(to_draw[i], center[i]) for i in range(2)]

        return to_draw

    @classmethod
    def get_sphere2D(cls, step: float, center: iter, radius: float) -> iter:
        is_shift = any(abs(i) > 10 * np.finfo(float).eps for i in center)
        is_scale = radius != 1
        return cls.__get_partit(step, is_shift=is_shift, center=center,
                                is_ellipse=is_scale, ab=(radius, radius))

    @classmethod
    def get_ellipse2D(cls, step: float, center: iter, ab: iter) -> iter:
        is_shift = any(abs(i) > 10 * np.finfo(float).eps for i in center)
        return cls.__get_partit(step, is_ellipse=True, ab=ab, is_shift=is_shift, center=center)
