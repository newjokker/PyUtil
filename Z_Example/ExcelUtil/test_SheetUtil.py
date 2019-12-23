# -*- coding: utf-8  -*-
# -*- author: jokker -*-

from Report.ExcelUtil import SheetUtil

# 实例化
a = SheetUtil()

table =  [[u'业务', u'状态', u'北京', u'上海', u'广州', u'深圳', u'状态小计', u'合计'],
            [00, 456, 789, 4444, u'1cc', u'jokker', u'hui', u'hvfw jhpv'],
            [u'gers', u'gre', u'gre', u'上海', u'广州', u'深圳', u'EEDWFWEFCEDW', u'合计'],
            [u'grea', u'gre', u'gre', u'CDS', u'gre', u'gre', u'状态小计', u'合计'],
            [u'业务', u'状态', u'北京', u'CDS', u'广州', u'gre', u'CDS', u'FCEDW']]

merge_info = [{'merge_value': u'标题', 'merge_range': (0,1,0,8)},
              {'merge_value': u'左标题', 'merge_range': (1,5,0,1)}]

# 设置列宽
a.column_width = 256*15
# 设置行高
a.row_height = 500
# 设置 table 信息
a.set_table(table)
# 设置 merge 信息
a.set_merge_info(merge_info)
# 保存至本地文件
a.save_to_book(r'C:\Users\Administrator\Desktop\hehe.xls', '第一个 sheet')

