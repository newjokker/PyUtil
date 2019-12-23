# -*- coding: utf-8  -*-
# -*- author: jokker -*-


from Report.ExcelUtil import SheetUtil
# import pandas as pd

a = SheetUtil(r'C:\Users\Administrator\Desktop\zaihai.xlsx')

data = a.get_table_info_from_sheet()

# df = pd.DataFrame(data)
# print(df)


# 获取数据
info = {}
for line_index, line in enumerate(data[1:]):
    key_01 = str(line_index+1).rjust(2, '0')
    for column_index, each in enumerate(line[2:]):
        if column_index == len(line[2:]) - 1:
            key_02 = '99'
        else:
            key_02 = str(column_index+1).rjust(2, '0')
        key = key_01 + key_02
        if each:
            info[key] = each

# 得到字典
dict_str = u'{'

for each in info:
    # dict_str += '"{0}": "{1}", '.format(each, info[each].encode('unicode-escape').decode('string_escape'))
    dict_str += u'"{0}": "{1}", '.format(unicode(each), info[each])

dict_str += u'}'

with open(r'C:\Users\Administrator\Desktop\aa.py', 'w') as txt_file:
    txt_file.write(dict_str)

print('-'*100)

