# -*- coding: utf-8  -*-
# -*- author: jokker -*-

"""我一直喜欢默认字典这个数据结构，后来一想这不就是 pandas 中的 DataFrame 数据结构吗？"""

# TODO 按照自己的方式实现默认数据字典
# TODO 使用 DataFrame 替换默认数据字典，看看是不是可行



import pandas as pd

data_frame = pd.DataFrame() # 用于存放所有的表格
data_frame = pd.concat([data_frame, DataManagementQH.format_data_frame(data_frame_temp)], axis=0)  # 连接两个 DataFrame， 竖过来拼接

# 从 excel 中获取 二维的表格 assign_table
assign_table = sheet_temp.get_table_info_from_sheet(year_str)
# 将二维的表格转为 DataFrame
data_frame_temp= pd.DataFrame(assign_table[1:], columns=assign_table[0])



# 切片，选择 DataFrame 结构中的几列数据
data_frame = data_frame[['csta','h11','h12','h13','fbday']]