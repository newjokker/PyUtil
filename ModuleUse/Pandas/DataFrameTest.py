# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import pandas as pd


# ------------------------------------------------ 创建 ----------------------------------------------------------------

a = [[1,2,3], [4,5,6], [7,8,9]]

data_frame_a = pd.DataFrame(a, index=['a', 'b', 'c'], columns=['aa', 'bb', 'cc'])
data_frame_b = pd.DataFrame(a, index=['a1', 'b1', 'c1'], columns=['aa', 'bb', 'cc1'])
data_frame_c = data_frame_a.append(data_frame_b, verify_integrity=True)

print(data_frame_c)
print(data_frame_b)

# ------------------------------------------------ 创建 ----------------------------------------------------------------




