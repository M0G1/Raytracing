import pathlib
import os

import view.matlab.sphere_ellipse_data2D as sphereEllipseReadWrite

# init correct path to files in program
cur_dir = pathlib.Path.cwd()
while "view" not in os.listdir(cur_dir):
    cur_dir = pathlib.Path(cur_dir.parent)

need_path = cur_dir / 'view' / 'matlab' / 'sphereEllipseSerialization'
sphereEllipseReadWrite.Sphere_Ellipse_data_2Dview._Sphere_Ellipse_data_2Dview__SERVICE_INFO_LOCATE = need_path
