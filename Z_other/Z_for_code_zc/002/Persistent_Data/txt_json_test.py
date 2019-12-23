# -*- coding: utf-8  -*-
# -*- author: jokker -*-


# import numpy as np
from ReadData.JsonUtil import JsonUtil

# a = np.array(range(100))
# a = a.reshape((10, 10))

save_path = r'D:\Code\Util_Util\Z_for_code_zc\002\data\123.txt'
# np.savetxt(save_path, a)

# a = np.loadtxt(save_path)

JsonUtil.save_data_to_json_file({"123": '123456',
                                 'jokker': 456789,
                                 'show': None},
                                r'E:\Algorithm\Util_Util\Z_for_code_zc\002\data\json.json')


