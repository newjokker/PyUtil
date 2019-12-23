# -*- coding: utf-8  -*-
# -*- author: jokker -*-

"""转移矩阵样式转变"""

from Report.ExcelUtil import SheetUtil, AddWorkBookUtil

# todo 多个裸地进行区分处理，后面加 _1


excel_path = r'C:\Users\Administrator\Desktop\表5-4  省级生态系统分布与构成转移矩阵（km2）.xlsx'
a = AddWorkBookUtil()

for page_index in range(3):
    table_info = SheetUtil(excel_path).get_table_info_from_sheet(sheet_index=page_index)
    res = [[u'省份', u'年代', u'类型', u'转换类型', u'面积']]
    for i in range(1, len(table_info)):
        year_from_to = table_info[i][1]  # 转换的时间
        for j in range(3, len(table_info[0])):
            from_type = table_info[i][2]
            to_type = table_info[0][j]
            change_area = table_info[i][j]
            res.append([u'江苏省', year_from_to, from_type, to_type, change_area])

    a.add_sheet(res, sheet_name='{0}级'.format(['一', '二', '三'][page_index]), width_adaptation=False)
a.save_to_book(r'C:\Users\Administrator\Desktop\del\转移矩阵样式转变.xls')
