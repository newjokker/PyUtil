# coding=utf-8
import os

# 输出excel文件的表头
tHead=[u'火区号',u'火点数',u'时间',u'经度',u'纬度',u'省',u'市',u'县',u'行政编号',u'最近杆塔编号',u'火点相对杆塔的方位和距离',u'最近的输电线路与线路距离',\
       u'明火面积(公顷)',u'土地类型',u'危害程度',u'卫星/传感器']


#=============H8 band contants==================

# allRes=['05','10','20','20','10','10'] 此次暂且将所有分辨率改为R10
allRes = ['10', '10', '10', '10', '10', '10']
# BandIndex = [33, 35] #
# numOfBands = 4
# creatTimeInd = [9, 22]

# 波段顺序：R 红外波段,NIR近红外波段,MIR中红外波段,FIR远红外波段
Bands = ['3', '4', '7', '14', '1', '2']

# 获取火点经纬度时多进程的数量
process_num = 4

# 输出文件名称格式
name_form = 'FIR_H8FIR_XCUR_ISSUE_COTM'

# 通过工程文件的相对路径获取所需的辅助文件
alo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
WGS_proj = alo_dir + os.sep + 'AuxData/GeoShp/sheng.prj'
WAE_prj = alo_dir + os.sep + 'AuxData/Target/WAE.prj'
area_border = alo_dir + os.sep + 'AuxData/GeoShp/sheng.shp'
tower_position = alo_dir + os.sep + 'AuxData/Target/point_identity.shp'
line_position = alo_dir + os.sep + 'AuxData/Target/line_WAE.shp'
land_use = alo_dir + os.sep + 'AuxData/Landuse/sichuan_dmj.tif'
mxd_1 = alo_dir + os.sep + 'AuxData/MXD/01SiChuan-ZT.mxd'
mxd_2 = alo_dir + os.sep + 'AuxData/MXD/02SiChuan-Pos.mxd'
FM_mask = alo_dir + os.sep + 'AuxData/Landuse/SCBigFM_WAE.shp'

mxd_shi_1 = alo_dir + os.sep + 'AuxData/MXD/01SiChuan-ZT_shi.mxd'
mxd_shi_2 = alo_dir + os.sep + 'AuxData/MXD/02SiChuan-Pos_shi.mxd'

# txt文件的属性表头
headInfo = '火区号' + ',' + '火点数' + ',' + '时间' + ',' + '经度' + ',' + '纬度' + ',' + '省' + ',' + '市' + ',' + '县' + ',' + '行政编号' + ',' + '火点最近杆塔编号' \
               + ',' + '火点相对杆塔的方位和距离' + ',' + '最近的输电线路与线路距离' + ',' + '明火面积' + ',' + '土地类型' + ',' + '危害程度' + ',' + '卫星/传感器'

# 读取结果矢量文件的表头
FieldList = "line_name; tower_numb; lon; lat; NEAR_DIST; NEAR_ANGLE; Cname; Xname; XID; NEAR_DIS_1; area"


# 计算背景温度时选用不同卷积核的大小
kernel_shp = [3,5,7,9,11] # 1KM
# kernel_shp = [7,9,11,13,15,17,19] # 2KM

# 火点判断系数
