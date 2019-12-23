# -*- coding: utf-8  -*-
# -*- author: jokker -*-

from Report.ExcelUtil import AddWorkBookUtil


Table =  [[u'业务', u'状态', u'北京', u'上海', u'广州', u'深圳', u'状态小计', u'合计'],
          [00, 456, 789, 4444, u'1cc', u'jokker', u'hui', u'hvfw jhpv'],
          [u'gers', u'gre', u'gre', u'上海', u'广州', u'深圳', u'EEDWFWEFCEDW', u'合计'],
          [u'grea', u'gre', u'gre', u'CDS', u'gre', u'gre', u'状态小计', u'合计'],
          [u'业务', u'状态', u'北京', u'CDS', u'广州', u'gre', u'CDS', u'FCEDW']]

mergeInfo = [{'merge_value': u'标题', 'merge_range': (0, 1, 0, 8)},
             {'merge_value': u'左标题', 'merge_range': (1,5,0,1)}]

b = AddWorkBookUtil()
# 设置信息
b.add_sheet(Table, merge_info=mergeInfo, sheet_name=u'面积', width_adaptation=False)
b.add_sheet(Table, merge_info=mergeInfo, sheet_name=u'比例', width_adaptation=False)

# 保存
b.save_to_book(r'C:\Users\Administrator\Desktop\111.xls')