# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import xlrd
import xlwt
from xlutils.copy import copy
from xlwt import Workbook, easyxf

# FIXME 设置边框，现在还不能，对一个范围的边框进行设置，调整每一个单元格的表框比较无语

# FIXME 写的行数不能太多，否者格式就会有问题

# TODO 将字竖过来排版

# TODO 预先指定表格的长宽

# TODO 改变指定行列的单元格样式，

# TODO 在merge info 中增加设置样式 {'merge_value': u'标题', 'merge_range': (0,1,0,8), 'merge_style': SheetCellStyle.get...}


class SheetCellStyle(object):
    """单元格的样式"""

    @staticmethod
    def get_style(font_style=(u'Times New Roman', 220, False, 1),
                  border=(0x01, 0x01, 0x01, 0x01),
                  border_color=(0x01, 0x01, 0x01, 0x01),
                  force_back_color=(0x40, 0x40, 0x40, 0x40),
                  mediate=(0x02, 0x01)):

        """获取样式"""

        # 字体的样式
        font_name, font_height, font_bold, font_color = font_style[:4]
        # 边框的样式
        border_top, border_bottom, border_left, border_right = border[:4]
        # 边框颜色
        border_top_color, border_bottom_color, border_left_color, border_right_color = border_color[:4]
        # 前后色
        pattern_fore_colour, pattern_back_colour = force_back_color
        # 水平、垂直居中
        mediate_horz, mediate_vert = mediate[:2]

        style = xlwt.XFStyle()
        # -- -- -- -- -- -- -- -- -- -- -- -- -- 字体 -- -- -- -- -- -- -- -- -- -- -- -- --
        font = xlwt.Font()
        font.name = font_name  # 'Times New Roman'
        font.bold = font_bold
        font.height = font_height
        font.color_index = font_color
        style.font = font
        # -- -- -- -- -- -- -- -- -- -- -- -- -- 边框 -- -- -- -- -- -- -- -- -- -- -- -- --
        borders = xlwt.Borders()
        # 边框样式
        borders.left = border_left
        borders.right = border_right
        borders.top = border_top
        borders.bottom = border_bottom
        borders.left = xlwt.Borders.THIN
        # 边框颜色
        borders.left_colour = border_left_color
        borders.right_colour = border_right_color
        borders.top_colour = border_top_color
        borders.bottom_colour = border_bottom_color
        style.borders = borders
        # -- -- -- -- -- -- -- -- -- -- -- -- -- 前后景 -- -- -- -- -- -- -- -- -- -- -- -- --
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = pattern_fore_colour
        pattern.pattern_back_colour = pattern_back_colour
        style.pattern = pattern
        # -- -- -- -- -- -- -- -- -- -- -- -- -- 居中 -- -- -- -- -- -- -- -- -- -- -- -- ---
        al = xlwt.Alignment()
        al.horz = mediate_horz
        al.vert = mediate_vert
        style.alignment = al

        return style

    @staticmethod
    def get_normal_style():
        """正常的样式"""
        # 字体
        font_name = u'宋体'
        font_height = 220
        font_bold = False
        font_color = 1
        font_style = font_name, font_height, font_bold, font_color
        # 边框
        border_top, border_bottom, border_left, border_right = 0x01, 0x01, 0x01, 0x01
        border = border_top, border_bottom, border_left, border_right
        # 边框颜色
        border_top_color, border_bottom_color, border_left_color, border_right_color = 0x40, 0x40, 0x40, 0x40
        border_color = border_top_color, border_bottom_color, border_left_color, border_right_color
        # 前后色
        pattern_fore_colour, pattern_back_colour = 0x41, 0x40
        force_back_color = pattern_fore_colour, pattern_back_colour
        # 水平居左，垂直居中
        mediate_horz, mediate_vert = 0x01, 0x01
        mediate = (mediate_horz, mediate_vert)
        # 设置样式
        need_style = SheetCellStyle.get_style(font_style, border, border_color, force_back_color, mediate)
        return need_style

    @staticmethod
    def get_title_style():
        """标题样式"""
        # 字体
        font_name = u'黑体'
        font_height = 300
        font_bold = True
        font_color = 1
        font_style = font_name, font_height, font_bold, font_color
        # 边框
        border_top, border_bottom, border_left, border_right = 0x01, 0x01, 0x01, 0x01
        border = border_top, border_bottom, border_left, border_right
        # 边框颜色
        border_top_color, border_bottom_color, border_left_color, border_right_color = 0x40, 0x40, 0x40, 0x40
        border_color = border_top_color, border_bottom_color, border_left_color, border_right_color
        # 前后色
        pattern_fore_colour, pattern_back_colour = 0x41, 0x40
        force_back_color = pattern_fore_colour, pattern_back_colour
        # 水平居左，垂直居中
        mediate_horz, mediate_vert = 0x02, 0x01
        mediate = (mediate_horz, mediate_vert)
        # 设置样式
        need_style = SheetCellStyle.get_style(font_style, border, border_color, force_back_color, mediate)
        return need_style

    @staticmethod
    def get_emphasize_style(color, border, mediate=False):
        """强调样式"""
        # 楷体
        # 加粗
        # 字号
        # 颜色
        # 居左


class SheetUtil(object):
    """excel 处理合集"""

    def __init__(self, work_book_path=None):
        self.sheet = None
        # 合并信息，按照输出的格式进行编写
        self.merge_info = []
        # 表格信息，存储为嵌套的列表
        self.table = []
        # 行的高度
        self.row_height = None
        # 列的宽度
        self.column_width = None

        # 获取 book
        if isinstance(work_book_path, xlrd.book.Book):
            self.book = work_book_path
        # elif isinstance(work_book_path, str) or isinstance(work_book_path, unicode):
        elif isinstance(work_book_path, str):
            self.book = xlrd.open_workbook(work_book_path)
        else:
            self.book = None
    # ----------------------------------- 设置属性 -------------------------------
    @staticmethod
    def set_column_style(sheet, column_indxe, column_width):
        """设置列属性"""
        # xlwt 中是行和列都是从0开始计算的
        first_col = sheet.col(column_indxe)
        # 256 * 20
        first_col.width = column_width

    @staticmethod
    def set_row_style(sheet, row_index, row_height):
        """设置行属性"""
        first_row = sheet.row(row_index)  # xlwt中是行和列都是从0开始计算的
        tall_style = xlwt.easyxf('font:height {0};'.format(row_height))  # 720 : 36pt
        first_row.set_style(tall_style)

    # ------------------------------------ 获取 --------------------------------

    def get_merge_info_from_sheet(self, sheet_name=None, sheet_index=0):
        """获取合并信息，保存的时候保存为输出的格式，这个函数的去留？"""

        if not self.book:
            return

        # 获取 sheet
        if sheet_name:
            self.sheet = self.book.sheet_by_name(sheet_name)
        elif sheet_index or sheet_index == 0:
            self.sheet = self.book.sheet_by_index(sheet_index)

        # 读取合并信息
        for each in self.sheet.merged_cells:
            cell_value = self.sheet.cell_value(each[0], each[2])
            # self.merge_info.append({'merge_value': unicode(cell_value), 'merge_range': each})
            self.merge_info.append({'merge_value': cell_value, 'merge_range': each})

    def get_table_info_from_sheet(self, sheet_name=None, sheet_index=0):
        """从 sheet 获取信息, table 信息，merge 信息"""

        if not self.book:
            return

        # 获取 sheet
        if sheet_name:
            self.sheet = self.book.sheet_by_name(sheet_name)
        elif sheet_index or sheet_index == 0:
            self.sheet = self.book.sheet_by_index(sheet_index)

        for i in range(self.sheet.nrows):
            self.table.append(self.sheet.row_values(i))
        return self.table

    def get_info_from_sheet(self):
        """获取数据"""
        # FIXME 获取合并信息的同时也要获取表格的样式

        # 合并信息
        self.get_merge_info_from_sheet()
        # 表身信息
        self.get_table_info_from_sheet()

    # ------------------------------------ 辅助函数 --------------------------------

    @staticmethod
    def len_byte(value):
        """获取字符串长度，一个中文的长度为2"""
        # value = unicode(value)
        length = len(value)*2
        utf8_length = len(value.encode('utf-8'))
        length = (utf8_length - length) / 2 + length
        return int(length)

    # ------------------------------------- 设置 -----------------------------------

    def set_merge_info(self, merge_info):
        """设置合并信息"""
        # 格式 [{'value': 123, 'range':(x, a, y, b), 'type':''}]
        if not isinstance(merge_info, list) or isinstance(merge_info, tuple):
            raise TypeError('* merge_info should be "list" or "tuple"')

        self.merge_info = merge_info

    def set_table(self, table):
        """设置表格信息"""
        # 格式 [[], [], []]，列表里面嵌套列表

        # 是否为列表
        if not isinstance(table, list):
            raise TypeError('* table should be a "list"')
        else:
            if not table:
                raise TypeError('* table is empty')

        # 是否每行宽度一致
        length_first = len(table[0])
        # 只有一行
        if len(table) <= 1:
            self.table = table
            return
        # 存在多行
        for each_line in table[1:]:
            if len(each_line) != length_first:
                raise TypeError('* every line in table should be as the same length')
        # 通过检查，赋值
        self.table = table

    def set_width_adaptation(self, sheet):
        """列宽度自适应"""
        # table 中无数据
        if not self.table:
            return

        # 得到 table 中每一列的宽度
        col_width = []
        for i in range(len(self.table)):
            for j in range(len(self.table[i])):
                if i == 0:
                    col_width.append(SheetUtil.len_byte(self.table[i][j]))
                else:
                    if col_width[j] < SheetUtil.len_byte(self.table[i][j]):
                        col_width[j] = SheetUtil.len_byte(self.table[i][j])

        # 设置 sheet 中每列的宽度
        for i in range(len(col_width)):
            if col_width[i] > 10:
                sheet.col(i).width = 256 * (col_width[i] + 1)

        return sheet

    # -------------------------------------- 写 -----------------------------------

    def write_table(self, sheet, cell_style=None):
        """写表身, 可选择数字字符串的改为数字"""
        # default = easyxf('font: name Arial;')  # define style out the loop will work  防止报 More than 4094 XFs (styles) 这个bug

        for i in range(0, len(self.table)):
            # 设置行高
            if self.row_height:
                # fixme 这边设置了每一行的高度，当文件比较大的时候就会报错，注释掉这边就行
                # SheetUtil.set_row_style(sheet, i, row_height=self.row_height)
                pass
            for j in range(0, len(self.table[0])):
                # 设置列宽
                if self.column_width:
                    SheetUtil.set_column_style(sheet, j, self.column_width)
                # 设置单元格样式
                if cell_style:
                    sheet.write(i, j, self.table[i][j], cell_style)
                else:
                    sheet.write(i, j, self.table[i][j])

        return sheet

    def write_merge_cell(self, sheet, merge_style=None):
        """写合并的单元信息"""
        # 写合并信息
        for each_merge in self.merge_info:
            vtemp = each_merge['merge_value']
            rtemp = each_merge['merge_range']
            if merge_style:
                sheet.write_merge(rtemp[0], rtemp[1]-1, rtemp[2], rtemp[3]-1, vtemp, merge_style)
            else:
                sheet.write_merge(rtemp[0], rtemp[1] - 1, rtemp[2], rtemp[3] - 1, vtemp)
        return sheet

    def save_to_book(self, book_path, sheet_name='sheet1'):
        """保存为 xls 文件"""

        # if not(isinstance(book_path, str) or isinstance(book_path, unicode)):
        #     raise TypeError('* book path is required')

        if not book_path.endswith('.xls'):
            raise TypeError('* can only be saved as xls file')

        work_book = xlwt.Workbook(encoding='utf-8')
        # 创建sheet
        sheet1 = work_book.add_sheet(sheet_name, cell_overwrite_ok=True)
        # 写表身信息
        self.write_table(sheet1, SheetCellStyle.get_normal_style())
        # 写合并信息
        self.write_merge_cell(sheet1, SheetCellStyle.get_title_style())
        # 列宽度自适应
        # self.set_width_adaptation(sheet1)

        # 保存文件
        work_book.save(book_path)
        #
        # print('* xls file have been saveed in {0}'.format(book_path))


class AddWorkBookUtil(object):
    """创建并新建多个sheet表"""

    def __init__(self):
        self.work_book = xlwt.Workbook(encoding='utf-8')
        pass

    def add_sheet(self, table, merge_info=None, sheet_name='new_sheet', column_width = 256 * 15, row_height = 500, width_adaptation=True):
        """增加表格"""
        # 实例化


        a = SheetUtil()
        # 创建sheet
        sheet1 = self.work_book.add_sheet(sheet_name, cell_overwrite_ok=True)
        # 设置信息
        a.column_width = column_width       # 设置列宽
        a.row_height = row_height           # 设置行高
        a.set_table(table)                  # 设置 table 信息
        # 合并信息
        if merge_info is not None:
            a.set_merge_info(merge_info)  # 设置 merge 信息
        # 写表身信息
        # a.write_table(sheet1, SheetCellStyle.get_normal_style())
        a.write_table(sheet1)
        # 写合并信息
        a.write_merge_cell(sheet1, SheetCellStyle.get_title_style())
        # 列宽度自适应
        if width_adaptation:
            a.set_width_adaptation(sheet1)

    def save_to_book(self, book_path):
        """保存为 excel 文件"""

        # if not(isinstance(book_path, str) or isinstance(book_path, unicode)):
        #     raise TypeError('* book path is required')

        if not book_path.endswith('.xls'):
            raise TypeError('* can only be saved as xls file')

        # 保存文件
        self.work_book.save(book_path)
        #
        # print('* xls file have been saveed in {0}'.format(book_path))


class UpdateWorkBookUtil(object):
    """从workbook 中替换指定sheet中的指定单元格"""

    def __init__(self, wb_path):
        self.work_book = xlrd.open_workbook(wb_path)

    def __get_sheet_index(self, sheet_name):
        """根据表格名返回表格的序号"""
        pass

    def update_assign_sheet(self, update_info):
        """更新指定work_book中的指定sheet， 因为这个方法只能用一次，所以需要"""
        self.work_book = copy(self.work_book)  # 类型为worksheet 无nrows 方法
        # 获取第一个 sheet
        for sheet_index in update_info:
            wbsheet_temp = self.work_book.get_sheet(sheet_index)
            # 替换
            for each_info in update_info[sheet_index]:
                wbsheet_temp.write(each_info[0], each_info[1], each_info[2])  # 从 0 开始， (列，行，替换后的值)

    def save_work_book(self, save_path):
        """保存 work_book"""
        self.work_book.save(save_path)


if __name__ == '__main__':

    a = SheetUtil(r'C:\Users\Administrator\Desktop\修正后的干图层数据\2003-2018年牧业区生态站资料统计（提供航天宏图版）.xls')
    table_info = a.get_table_info_from_sheet()

    print(table_info)

    """
    ### 完善
    
    * 结合 Add 模式和 Update 模式 两部分，在对 excel 操作的时候，既能替换也能更新
        * 在执行 Update 的时候，先不执行，先把需要执行的步奏记录在内存中
        * 先执行 Add 模式的内容，保存为 save_path 路径
        * 对路径保存的文件再次进行读取，再去执行替换操作即可
    
    * 如何设置指定区域一定的格式，
    
    ### 流水
    
    * 增加表格更新模式 : https://www.cnblogs.com/jiangzhaowei/p/6179759.html
    
    """
