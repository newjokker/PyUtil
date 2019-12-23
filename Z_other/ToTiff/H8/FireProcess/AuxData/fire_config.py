# -*- coding: utf-8 -*-
# author：ChenQiang time:2019/1/30

import os


class ConfigPara:

    """H8火情监测中的配置参数"""
    # 计算背景温度时选用不同卷积核的大小
    kernel_shp = [3, 5, 7, 9, 11]  # 2KM
    # kernel_shp = [7,9,11,13,15,17,19] # 1KM

    # 火点判断系数
    refine_mir_fire = 3.5
    refine_m_f_fire = 3

    # 输出文件名称格式
    name_form = 'FIR_H8FIR_XCUR_ISSUE_COTM_SiChuan'

    # 读取结果矢量文件的表头
    FieldList = "line_name; tower_numb; lon; lat; NEAR_DIST; NEAR_ANGLE; Cname; Xname; XID; NEAR_DIS_1; area"

    # 生成业务txt文件的属性表头
    headInfo = '火区号' + ',' + '火点数' + ',' + '时间' + ',' + '经度' + ',' + '纬度' + ',' + '省' + ',' + '市' + ',' + '县' + ',' + '行政编号' + ',' + '火点最近杆塔编号' \
               + ',' + '火点相对杆塔的方位和距离' + ',' + '最近的输电线路与线路距离' + ',' + '明火面积' + ',' + '土地类型' + ',' + '危害程度' + ',' + '卫星/传感器'

    # 输出业务excel文件的表头
    tHead = [u'火区号', u'火点数', u'时间', u'经度', u'纬度', u'省', u'市', u'县', u'行政编号', u'最近杆塔编号', u'火点相对杆塔的方位和距离',
             u'最近的输电线路与线路距离',u'明火面积(公顷)', u'土地类型', u'危害程度', u'卫星/传感器']


    auxdata_dir = os.path.abspath(os.path.dirname(__file__))
    WGS_prj = auxdata_dir + os.sep + 'AuxData/GeoShp/sheng.prj'
    WAE_prj = auxdata_dir + os.sep + 'AuxData/Target/WAE.prj'
    area_border = auxdata_dir + os.sep + 'AuxData/GeoShp/sheng.shp'
    tower_position = auxdata_dir + os.sep + 'AuxData/Target/point_identity.shp'
    line_position = auxdata_dir + os.sep + 'AuxData/Target/line_WAE.shp'
    land_use = auxdata_dir + os.sep + 'AuxData/Landuse/sichuan_dmj.tif'
    FM_mask = auxdata_dir + os.sep + 'AuxData/Landuse/SCBigFM_WAE.shp'

    #
    sheng_them_mxd = auxdata_dir + os.sep + 'AuxData/MXD/sheng_SiChuan-ZT.mxd'
    # huodian
    sheng_pos_mxd = auxdata_dir + os.sep + 'AuxData/MXD/sheng_SiChuan-Pos.mxd'
    #
    sheng_mir_mxd = auxdata_dir + os.sep + 'AuxData/MXD/sheng_SiChuan-Mir.mxd'
    shi_them_mxd = auxdata_dir + os.sep + 'AuxData/MXD/shi_SiChuan-ZT.mxd'
    shi_pos_mxd = auxdata_dir + os.sep + 'AuxData/MXD/shi_SiChuan-Pos.mxd'
    shi_mir_mxd = auxdata_dir + os.sep + 'AuxData/MXD/shi_SiChuan-Mir.mxd'


    # H8波段文件的固定常量
    chltag = ['B01', 'B02', 'B03', 'B04', 'B05', 'B06',
              'B07', 'B08', 'B09', 'B10', 'B11', 'B12',
              'B13', 'B14', 'B15', 'B16']

    segTag = ['S01', 'S02', 'S03', 'S04', 'S05', 'S06', 'S07', 'S08', 'S09', 'S10', 'S11', 'S12', 'S13', 'S14',
              'S15', 'S16']

    resTag = ['R10', 'R10', 'R05', 'R10', 'R20', 'R20', 'R20', 'R20', 'R20', 'R20', 'R20',
              'R20', 'R20', 'R20', 'R20', 'R20']


    # xml结果的状态
    log_info = ['error','success','success']



if __name__ == '__main__':
    curPath = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    print ''
