import pathlib
import os

import view.sphereEllipseReadWrite as sphereEllipseReadWrite


# init correct path to files in program
cur_dir = pathlib.Path.cwd()
while "view" not in os.listdir(cur_dir):
    cur_dir = pathlib.Path(cur_dir.parent)

need_path = cur_dir / "view" / 'sphereEllipseSerialization'
sphereEllipseReadWrite.Sphere_Ellipse_data_2Dview._Sphere_Ellipse_data_2Dview__SERVICE_INFO_LOCATE = need_path
