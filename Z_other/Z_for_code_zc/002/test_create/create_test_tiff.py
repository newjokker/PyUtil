# -*- coding: utf-8  -*-
# -*- author: jokker -*-

from Report.GdalUtil import GdalBase
import numpy as np


def create_test_tiff(im_data, angle_point_lon, angle_point_lat, cell_size, save_path, no_data_value):
    """生产测试 tiff"""
    # 坐标系统
    im_proj = GdalBase.get_proj('WGS84')
    # 6 参数
    im_geotrans = (angle_point_lon, cell_size, 0.0, angle_point_lat, 0.0, -cell_size)
    #
    height, width = im_data.shape
    # 生成 tiff
    GdalBase.write_tiff(im_data, width, height, 1, im_geotrans, im_proj,
                        out_path=save_path, no_data_value=no_data_value)


if __name__ == "__main__":

    save_tiff_path = r'E:\Algorithm\Util_Util\Z_for_code_zc\002\data\456.tif'
    im_array = np.arange(200).reshape(20, 10).astype(np.int16)
    create_test_tiff(im_array, 100, 30, 0.05, save_tiff_path, -999)




