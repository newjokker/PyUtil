# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import os


def ldf_to_tiff(env_path, in_ldf, save_tiff_path):
    os.chdir(env_path)
    os.system("gdal_translate -of" + " " + "GTiff" + " " + in_ldf + " " + save_tiff_path)


if __name__ == "__main__":

    envPath = r'D:\Code\Util_Util\Z_other\ToTiff\ldf\fy3mwhsx_wgs84-package\bin'
    inLdf = r'C:\Users\Administrator\Desktop\del\test\FY3B_MERSI_WHOLE_GLL_L1_20191111_1508_1000M.ldf'
    saveTiffPath = r'C:\Users\Administrator\Desktop\del\del\123.tif'
    ldf_to_tiff(envPath, inLdf, saveTiffPath)


