# -*- coding: utf-8  -*-
# -*- author: jokker -*-

from Report.MySqlUtil import MySqlUtil
from Report.ExcelUtil import SheetUtil

# # 拿到需要插入的数据
# a = SheetUtil(r'C:\Users\Administrator\Desktop\aa.xls')
# data = a.get_table_info_from_sheet(sheet_index=0)
# db_info = []
# for line in data:
#     crop = line[0]
#     station_name = line[1]
#     process = ','.join(line[2:])
#     db_info.append({'crop': crop, 'station_name': station_name, 'process': process})


# 插入数据
a = MySqlUtil()
host, port, user, passwd, db_name = 'localhost', 3306, 'root', '747225581', "test_del"
a.conoect_mysql(host, port, user, passwd, db_name)

db_info = []
for i in range(10):
    db_info.append({'id': i, 'name': str(i**2)})

# 插入数据会遇到编码的问题，这个比较难以解决
a.insert_info_to_table('test', db_info)


