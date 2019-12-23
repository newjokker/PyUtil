# -*- coding: utf-8  -*-
# -*- author: jokker -*-

from Report.MySqlUtil import MySqlUtil


a = MySqlUtil()

# a.conoect_mysql('localhost', 3306, 'root', '747225581', 'jokker')
a.conoect_mysql('localhost', 3306, 'root', '747225581', 'world')

# data = a.get_info_from_database(['content', 'tags'], 'duanzi', None)
#
# for each in data:
#     print(each)
#

data = a.execute_and_fetch('select language from countrylanguage where language = "chinese"')

print(data)
