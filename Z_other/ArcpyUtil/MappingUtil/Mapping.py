# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import arcpy
import os
import logging

class MappingPicture(object):
    """arcpy mapping 模块出图"""

    def __init__(self, mxd_path=None):

        # mxd 路径
        self.mxd_path = mxd_path
        # mxd 对象
        self.mxd = None
        # 需要修补的图层字典
        self.replace_layer_info = None
        # 需要拿到的 shp 中的属性
        self.page_row_info = None
        # ☆ 替换文字列表，出现中文见面要加 u, 变为 unicode
        self.text_element_info = {}
        # 出图的类型 支持 jpg 和 png 两种
        self.pic_type = 'jpg'
        # 出图分辨率
        self.resolution = 600
        # 保存文件夹
        self.save_folder = None
        # 保存文件名
        self.save_name = None
        # 强行不使用驱动页
        self.force_not_use_driven_page = False
        # 是否缺失图层
        self.__need_fix_mxd = False
        # 是否使用 drive_page 每一个区域出一张图
        self.__use_driven_page = False
        # 是否修复文字
        self.__need_fix_text = False
        # 需要修补的图层
        self.__need_fix_layers = None
        # 出图参数检查结果
        self.__check_result = False
        #
        self.textElement_model = {}
        # 指定出图的范围, {'loc_x':123, 'loc_y':25, 'length':5}
        self.assign_extent = None
        # 指定缩放至的图层
        self.assign_layer_extent_name = None
        # 指定 drive 需要出的图
        self.assign_drive_page_dict = None

    def map_init(self):
        """准备工作"""
        # 载入对象
        if self.mxd_path:
            self.mxd = arcpy.mapping.MapDocument(self.mxd_path)
        # --------------------------------------------------------------------------------------------------------------
        # 检查 mxd 对象
        if not self.mxd:
            print('need correct mxd path or mxd object')
            return
        # --------------------------------------------------------------------------------------------------------------
        # 设置范围
        if self.assign_extent:
            DF = self.mxd.activeDataFrame
            DF_extent = DF.extent
            # 获取范围参数
            loc_x = self.assign_extent['loc_x']
            loc_y = self.assign_extent['loc_y']
            length = self.assign_extent['length']
            if 'height' in self.assign_extent:
                height = self.assign_extent['height']
            else:
                height = None
            # 获取需要的范围
            DF_extent.XMin, DF_extent.XMax, DF_extent.YMin, DF_extent.YMax = MappingPicture.get_zoom_extent((loc_x, loc_y), length, height=height)
            # 设置范围
            DF.extent = DF_extent
        # --------------------------------------------------------------------------------------------------------------
        # 检查文件名
        if not (self.save_folder and self.save_name):
            logging.error('need save dir')
            return
        else:
            if not os.path.exists(self.save_folder):
                logging.error('save path is illegal')
                return
        # --------------------------------------------------------------------------------------------------------------
        # 检查是否需要修补图层
        self.__need_fix_layers = arcpy.mapping.ListBrokenDataSources(self.mxd)
        if self.__need_fix_layers:
            self.__need_fix_mxd = True
            # 查看需要修补的图层是否都有
            for each_layer in self.__need_fix_layers:
                # 可能不是 layer 图层
                if not isinstance(each_layer, arcpy._mapping.Layer):
                    continue
                if not each_layer.supports("DATASOURCE") and each_layer.name in self.replace_layer_info:
                    print('lose layer')
                    return
        # 检查 文字是否需要修复
        if self.text_element_info:
            self.__need_fix_text = True
        # 检查出来的图片的格式
        if not self.pic_type.strip('.').upper() in ['JPG', 'PNG']:
            print('image type should be jpg or png')
            return
        # --------------------------------------------------------------------------------------------------------------
        # 检查是否支持驱动页
        if hasattr(self.mxd, 'dataDrivenPages'):
            self.__use_driven_page = True
        # --------------------------------------------------------------------------------------------------------------
        # 记录原始模板，因为后面会对模板进行替换，所以需要在这边将原始模板记录下来
        for textElement in arcpy.mapping.ListLayoutElements(self.mxd, "TEXT_ELEMENT"):
            # 过滤字典中没有的替换文字
            if textElement.name not in self.text_element_info:
                continue
            self.textElement_model[textElement.name] = textElement.text

        self.__check_result = True
        # 返回检查结果
        return self.__check_result

    def fix_mxd(self):
        """修补 mxd 中的缺失图层"""

        for broken_lyr in self.__need_fix_layers:
            # 替换图层, dstWorkspace:所在文件夹，文件类型，lyrRSName：文件名

            # 过滤字典中没有的坏图层
            if broken_lyr.name not in self.replace_layer_info:
                continue

            replace_path = self.replace_layer_info[broken_lyr.name]
            folder, file_name = os.path.split(replace_path)
            suffix = os.path.splitext(file_name)[1]
            if suffix in ['.tif']:
                broken_lyr.replaceDataSource(folder, "RASTER_WORKSPACE", file_name)
            elif suffix in ['.shp']:
                # 文件存在替换
                broken_lyr.replaceDataSource(folder, "SHAPEFILE_WORKSPACE", file_name[:-4])

        print('* fix layer success')

        # FIXME  主动添加图层，看看为什么会无法显示
        # 引用当前活动的地图文档
        # mxd = self.mxd
        # 获取对Layers(所有图层在数据框下面)数据框的引用。
        # df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]
        # 定义参考图层
        # refLayer = arcpy.mapping.ListLayers(mxd, "Burglaries*", df)[0]
        # 定义相对于参考图层的插入图层
        # insertLayer = arcpy.mapping.Layer(r"C:\Users\Administrator\Desktop\H8\temp\a0224040-5c02-11e9-8db4-6c4b905b11db\background_rgb.tif")
        # insertLayer = arcpy.mapping.Layer(r"C:\Users\Administrator\Desktop\background_rgb.tif.lyr")
        # 插入图层
        # arcpy.mapping.AddLayer(df, insertLayer, "BOTTOM")
        # arcpy.mapping.AddLayer(df, insertLayer, "AUTO_ARRANGE")

    def zoom_to_assign_lyr(self):
        """扩大到指定图层的范围"""

        if not self.assign_layer_extent_name:
            return

        layers = arcpy.mapping.ListLayers(self.mxd)

        for layer in layers:
            if layer.name == self.assign_layer_extent_name:
                self.mxd.activeDataFrame.extent = layer.getSelectedExtent()
                break

    def change_df_scale(self):
        """改变出图的数据框的大小"""

        # FIXME 如何获取整幅图的长度宽度，再指定数据框的长度宽度

        # eg:if the scale is 1:10000 ， please input 10000
        my_scale = arcpy.GetParameterAsText(0)
        zm_lyr = arcpy.GetParameterAsText(1)
        # 得到数据框
        df = arcpy.mapping.ListDataFrames(self.mxd)[0]
        lyrs = arcpy.mapping.ListLayers(self.mxd_path, str(zm_lyr) ,df)
        lyr = lyrs[6]
        # 选中需要全部显示的图层中要素
        my_scale = 20000
        df.scale = my_scale # set 10000 or others scale and calculation range

        print self.mxd.pageSize

        # start make my setting
        df.elementHeight = 13
        df.elementWidth = 16
        df.panToExtent(lyr.getExtent())

    def change_title_txt(self, now_page_info=None):
        """修补出图模板中的文字部分"""
        # 遍历所有 TEXT_ELEMENT 类型
        for textElement in arcpy.mapping.ListLayoutElements(self.mxd, "TEXT_ELEMENT"):
            # 过滤字典中没有的替换文字
            if textElement.name not in self.text_element_info:
                continue

            replace_dict = self.text_element_info[textElement.name]
            # 因为之前的模板被替换，所以只能先将模板保存下来，否者出来的图都是一样的
            element_text = self.textElement_model[textElement.name]
            # ----------------------------------------------------------------------------------------------------------
            # ☆ 使用传入的字典替换 element_text 属性（优先级比较高，因为这个是可以控制的，而传入的属性不能控制）
            for each_attr in replace_dict:
                element_text = element_text.replace('{' + each_attr + '}', replace_dict[each_attr])
                # element_text = element_text.replace('{' + each_attr + '}', str(replace_dict[each_attr]))
            # ----------------------------------------------------------------------------------------------------------
            # 使用 drive 当前属性替换 element_text
            if self.__use_driven_page and now_page_info:
                for each_attr in now_page_info:
                    element_text = element_text.replace('{' + each_attr + '}', now_page_info[each_attr])
                    # element_text = element_text.replace('{' + each_attr + '}', str(now_page_info[each_attr]))
            # ----------------------------------------------------------------------------------------------------------
            # 替换元素
            textElement.text = element_text
            print('* replace text success')

    @staticmethod
    def get_save_name(name_template, now_page_info=None):
        """获取保存文件名"""
        for each_attr in now_page_info:
            name_template = name_template.replace('{' + each_attr + '}', now_page_info[each_attr])
        return name_template

    @staticmethod
    def get_zoom_extent(point_xy, length, height=None):
        """
        获取局部放大图的范围
        :param height: 高
        :param point_xy: 中心点经纬度
        :param length: 半径大小，或者长
        :return: 局部放大图范围上下左右
        """
        # 如果不指定高度的话就认为高度等于宽度
        if height is None:
            height = length

        # 解析经纬度
        loc_x = point_xy[0]
        loc_y = point_xy[1]
        # 得到经纬度范围
        loc_x_min = loc_x - length
        loc_x_max = loc_x + length
        loc_y_min = loc_y - height
        loc_y_max = loc_y + height
        # 返回经纬度范围
        return loc_x_min, loc_x_max, loc_y_min, loc_y_max

    def use_this_page(self):
        """是否使用当前页面"""
        if self.assign_drive_page_dict is None:
            return True

        for each_attr in self.assign_drive_page_dict:

            if hasattr(self.mxd.dataDrivenPages.pageRow, each_attr):
                attr_val = self.mxd.dataDrivenPages.pageRow.getValue(each_attr)
                if attr_val in self.assign_drive_page_dict[each_attr]:
                    return True

    def get_pic(self):
        """出图"""
        if self.__use_driven_page and not self.force_not_use_driven_page:
            # 使用驱动页
            for pageNum in range(1, self.mxd.dataDrivenPages.pageCount + 1):
                # ------------------------------------------------------------------------------------------------------
                # 设置当前页面
                self.mxd.dataDrivenPages.currentPageID = pageNum
                # ------------------------------------------------------------------------------------------------------
                # 是否使用当前的驱动页
                if not self.use_this_page():
                    continue
                # ------------------------------------------------------------------------------------------------------
                # 获取需要的属性
                now_page_info = {}
                for each_att in self.page_row_info:
                    arrt_name = self.page_row_info[each_att]
                    # 变量名和属性表中当前 drivepage 所用的变量名一样的时候，使用属性名
                    now_page_info[each_att] = self.mxd.dataDrivenPages.pageRow.getValue(arrt_name)
                # ------------------------------------------------------------------------------------------------------
                # 修复文字
                if self.__need_fix_text:
                    self.change_title_txt(now_page_info)
                # ------------------------------------------------------------------------------------------------------
                # save_name 模板进行替换
                save_name = self.get_save_name(self.save_name, now_page_info)
                save_path = os.path.join(self.save_folder, save_name + '.' + self.pic_type.strip('.'))
                # 新建文件保存文件夹，这样保存结果就能支持保存在特定的结构目录中去了，目录可以根据属性生成
                save_dir = os.path.dirname(save_path)
                if not os.path.exists(save_dir): os.makedirs(save_dir)
                # ------------------------------------------------------------------------------------------------------
                # 缩放至图层
                # self.zoom_to_assign_lyr()
                # ------------------------------------------------------------------------------------------------------
                # 出图
                if self.pic_type.upper() == 'JPG':
                    arcpy.mapping.ExportToJPEG(self.mxd, save_path, resolution=self.resolution)
                else:
                    arcpy.mapping.ExportToPNG(self.mxd, save_path, resolution=self.resolution)
                print('* get picture {0} success'.format(str(pageNum).rjust(4, '0')))
        else:
            # ----------------------------------------------------------------------------------------------------------
            # 不使用驱动页面
            if self.__need_fix_text:
                # 修复文字
                self.change_title_txt()
            save_path = os.path.join(self.save_folder, self.save_name + '.' + self.pic_type.strip('.'))
            save_dir = os.path.dirname(save_path)
            if not os.path.exists(save_dir): os.makedirs(save_dir)
            # ----------------------------------------------------------------------------------------------------------
            # 缩放至图层，不能缩放至修复的图层，所以先不考虑使用这个函数
            # self.zoom_to_assign_lyr()
            # ----------------------------------------------------------------------------------------------------------
            # 出图
            if self.pic_type.upper() == 'JPG':
                arcpy.mapping.ExportToJPEG(self.mxd, save_path, resolution=self.resolution)
            else:
                arcpy.mapping.ExportToPNG(self.mxd, save_path, resolution=self.resolution)

    def do_process(self):
        """主流程"""
        # 检查
        if not self.map_init():
            print('error in init check')
        # 图层修复
        if self.__need_fix_mxd:
            self.fix_mxd()
        # 改变数据框的大小
        # self.change_df_scale()
        # 出图
        self.get_pic()


if __name__ == "__main__":

    # FIXME 出不了图，对图层进行金字塔的统计，【没有金字塔就没有统计，就不会有问题】
    # arcpy.BuildPyramidsandStatistics_management(rgb_path)
    # FIXME 解析 china.xml 将结构放到合适的结构中，以后就不要变了


    # FIXME 自动生成 legend 带着不同的色块，给分类 tiff 插入不同的颜色，完成自动的 mxd 生成

    # FIXME 增加替换图层模式，替换未破损图层


    # mxd_path = r'C:\Users\Administrator\Desktop\China-Them.mxd'
    # a = MappingPicture(mxd_path)
    # a.resolution = 300
    # a.pic_type = 'png'
    # a.replace_layer_info = {'mir.tif': r'C:\Users\Administrator\Desktop\H8\temp\b75a58d1-66eb-11e9-ac55-6c4b905b11db\enhance_B07.tif'}
    # a.page_row_info = {u'Name': u'Name', u'ID':u'ID'}
    # a.text_element_info = {'titlename': {u'hehe':'4456'}}
    # a.save_folder = r'C:\Users\Administrator\Desktop\npp_test'
    # a.save_name = u'{Name}_{ID}专题图'
    # # 指定数据框范围
    # a.assign_extent = {'loc_x':101.58, 'loc_y':28.40, 'length':3}
    # # 图像缩放至指定的图层
    # a.assign_drive_page_dict = {'Name':[u'北京市', u'湖北省'], 'ID':['520000000000'],'ok':['gre']}
    # a.do_process()

    # # 使用东部农区的矢量进行裁剪
    # raster = r'C:\Users\Administrator\Desktop\白琳\test.tif'
    # shp = r'C:\Users\Administrator\Desktop\DBNT\DBNT.shp'
    # a = arcpy.sa.ExtractByMask(raster, shp)
    # a.save(r'C:\Users\Administrator\Desktop\DBNT\DBNT.tif')

    arcpy.BuildPyramidsandStatistics_management(r'C:\Users\Administrator\Desktop\bl\test.tif')


    mxd_path = r'C:\Users\Administrator\Desktop\bl\bailin.mxd'
    a = MappingPicture(mxd_path)
    a.force_not_use_driven_page = True
    a.resolution = 300
    a.pic_type = 'png'
    # a.replace_layer_info = {'test': r'C:\Users\Administrator\Desktop\bl\tif1_new.tif'}
    a.replace_layer_info = {'test': r'C:\Users\Administrator\Desktop\bl\test.tif'}

    a.page_row_info = {u'Name': u'Name', u'ID':u'ID'}
    a.text_element_info = {'title': {u'X':'4456'},
                           'info':{'yyyy':'123', 'mm':'34'},
                           'date':{'yyyy':'444', 'mm':'435', 'dd':'456'}}
    a.save_folder = r'C:\Users\Administrator\Desktop'
    a.save_name = u'{Name}_{ID}专题图'
    # 指定数据框范围
    # a.assign_extent = {'loc_x':101.58, 'loc_y':28.40, 'length':3}
    # 图像缩放至指定的图层
    # a.assign_drive_page_dict = {'Name':[u'北京市', u'湖北省'], 'ID':['520000000000'],'ok':['gre']}
    a.do_process()


"""
1. 要想在输出文件名或者替换文字中使用 drivepage 中的属性值，首先需要完善 replace_layer_info 信息，{u'Name': u'Name', u'ID':u'ID'}
2. assign_layer_extent_name, 缩放至指定图层范围，先关闭使用
3. self.mxd.pageSize 是只读属性不能改变大小，所以函数 change_df_scale 只用于改变 数据框大小
"""