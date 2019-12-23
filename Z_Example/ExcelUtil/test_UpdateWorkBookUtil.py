# -*- coding: utf-8  -*-
# -*- author: jokker -*-

from Report.ExcelUtil import UpdateWorkBookUtil

c = UpdateWorkBookUtil(r'C:\Users\Administrator\Desktop\123.xlsx')

c.update_assign_sheet({0: [(1, 2, u"呵呵")],
                       1: [(5, 10, u"再说")],
                       2: [(12,12, 4567897433543)]})

c.save_work_book(r'C:\Users\Administrator\Desktop\123.xls')