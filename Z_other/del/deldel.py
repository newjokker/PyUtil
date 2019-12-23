# -*- coding: utf-8  -*-
# -*- author: jokker -*-


from ReadData.PickleUtil import PickleUtil
from Report.ExcelUtil import SheetUtil

Crop_Jieyi_Info = PickleUtil.load_data_from_pickle_file(r'C:\Users\Administrator\Desktop\CX\123.pkl')

# Crop_Jieyi_Info  = Crop_Jieyi_Info[13:40]
Crop_Jieyi_Info  = Crop_Jieyi_Info

temp = [None, None]
info_now = []  # 时间列表
info_index = None

for line_index, each_line in enumerate(Crop_Jieyi_Info):

    station, crop, date_str = each_line[0], each_line[1], each_line[-1]

    if temp[0] == station and temp[1] == crop:
        print('same station')
        # 将不存在的数据进行合并
        if date_str not in info_now:
            info_now.append(date_str)
            # 删除当前 datestr
        Crop_Jieyi_Info[line_index][-1] = ''
    else:
        print('write data')
        # 删除当前 datestr
        Crop_Jieyi_Info[line_index][-1] = ''

        if info_index is not None:
            # 修改前面info信息
            print('write line {0}'.format(info_index))
            Crop_Jieyi_Info[info_index][-1] = ','.join(info_now)
            info_now = [date_str]  # 重置 datastr

        info_index = line_index  # 将新开的一行位置传给变量

    temp = [station, crop]  # 将本行信息作为下一行的上一行信息进行存储

Crop_Jieyi_Info[info_index][-1] = ','.join(info_now)

for each_line in Crop_Jieyi_Info:
    print(each_line[0:2], each_line[-1])
    # print(each_line[-1])

a = SheetUtil()

# 设置列宽
a.column_width = 256*15
# 设置行高
a.row_height = 500
# 设置 table 信息
a.set_table(Crop_Jieyi_Info)
# 保存至本地文件
a.save_to_book(r'C:\Users\Administrator\Desktop\CX\cx_table.xls', u'第一个 sheet')


