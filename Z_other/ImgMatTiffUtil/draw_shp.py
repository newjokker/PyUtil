# -*- coding: utf-8  -*-
# -*- author: jokker -*-

from Function.GdalUtil import CreateOgr, OgrBase, GdalBase, GdalTools
from ImageUtil import ImageUtil, ImageMapping


# ------------------------------------- 信息转点 ----------------------------
def get_middle_point(line_info):
    """得到各个线矢量的中心点"""
    point_loc_lonlat = []
    point_info = []
    for each in line_info:
        point_info_temp = {}
        x, y = zip(*each['points'])
        # name = each['CNAME']
        name = each['CID'][:4]
        # name = str(each['ORIG_FID'])
        point_info_temp['lon'] = (min(x) + max(x)) / 2
        point_info_temp['lat'] = (min(y) + max(y)) / 2
        point_info_temp['name'] = name
        point_info.append(point_info_temp)
        point_loc_lonlat.append(((min(x) + max(x)) / 2, (min(y) + max(y)) / 2))

    # CreateOgr.create_points_from_dict(point_info, r'C:\Users\Administrator\Desktop\依赖注入\shi_point.shp', lon_string='lon', lat_string='lat')
    return point_loc_lonlat, point_info


# 输入面矢量
# 面-->栅格-->矩阵
# 得到点坐标，点标签
# 生成标签文字
# 根据点坐标计算粘贴位置（行列坐标）
# 粘贴标签文字
# 出图


if __name__ == '__main__':

    line_shp = r'C:\Users\Administrator\Desktop\del\shi_line.shp'
    # 转栅格
    line_tiff = OgrBase.shp_to_tif(line_shp, None, 0.01, shp_attribute=None, return_mode='MEMORY')
    # 获取线中点数据
    line_info = CreateOgr.convert_polyline_to_dict(line_shp)
    # 得到中心点坐标
    point_loc_lonlat, point_info = get_middle_point(line_info)
    # 得到中心点行列号
    point_loc_xy = GdalTools.extract_loc_xy_in_tiff(line_tiff, point_loc_lonlat)
    # tiff 转矩阵
    line_mat = GdalBase.read_tiff(line_tiff)[0]
    # 新建色彩表
    legendInfo = [
        {'color': (255, 255, 255), 'data': u'一级别', 'value': 0},
        {'color': (255, 0, 0), 'data': u'二级别', 'value': 255}, ]
    # 转为图像矩阵
    image_mat = ImageMapping.tiff_to_image_mat(line_tiff, legend_info=legendInfo)

    # 得到
    for index, each_xy in enumerate(point_loc_xy):
        image_mat[each_xy[0], each_xy[1], :3] = 0
        name = point_info[index]['name']
        # 文字转为图片
        word_mat_temp = ImageUtil.create_word_img(name, word_size=25, word_color=(0, 0, 0))
        # 绘画
        assign_loc = (
        each_xy[0] - int((word_mat_temp.shape[0] / 2.0)), each_xy[1] - int((word_mat_temp.shape[1] / 2.0)))
        ImageUtil.draw(image_mat, word_mat_temp, assign_loc=assign_loc)

    ImageUtil.save_to_image(image_mat, r'C:\Users\Administrator\Desktop\A.png')
