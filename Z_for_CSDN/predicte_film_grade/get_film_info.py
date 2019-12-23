# -*- coding: utf-8  -*-
# -*- author: jokker -*-

"""获取电影信息"""

import os
from Report.MySqlUtil import MySqlUtil
from ReadData.PickleUtil import PickleUtil
from Z_for_CSDN.predicte_film_grade.FunctionFilmGrade.ParseFilmInfo import ParseFilmInfo


if __name__ == '__main__':

    # film_info_list = []
    #
    # a = ParseFilmInfo()
    # for each_html_path in os.listdir(r'E:\Algorithm\Util_Util\Z_for_CSDN\predicte_film_grade\aux_data\htmls'):
    #     abs_html_path = os.path.join(r'E:\Algorithm\Util_Util\Z_for_CSDN\predicte_film_grade\aux_data\htmls', each_html_path)
    #     film_info = a.parse_film_info_001(abs_html_path)
    #     film_info_list.append(film_info)
    # PickleUtil.save_data_to_pickle_file(film_info_list, r'E:\Algorithm\Util_Util\Z_for_CSDN\predicte_film_grade\aux_data\film_info\film_info.pkl')

    a = ParseFilmInfo()
    # a.config_dir = r'D:\Code\Util_Util\Z_for_CSDN\predicte_film_grade\aux_data\config'
    a.config_dir = r'E:\Algorithm\Util_Util\Z_for_CSDN\predicte_film_grade\aux_data\config'
    a.load_config_info()

    pkl_path = r'E:\Algorithm\Util_Util\Z_for_CSDN\predicte_film_grade\aux_data\film_info\film_info.pkl'
    film_info_list = PickleUtil.load_data_from_pickle_file(pkl_path)
    film_info_list = list(filter(lambda x: len(x), film_info_list))

    # 3587, 2864
    search_film_info_list = []
    for each in film_info_list:
        film_info = a.get_film_info_from_film_dict(each)
        search_film_info_list.append(film_info)
        print(film_info)

    # 插入数据
    a = MySqlUtil()
    host, port, user, passwd, db_name = 'localhost', 3306, 'root', '747225581', "test_del"
    a.conoect_mysql(host, port, user, passwd, db_name)

    # 插入数据会遇到编码的问题，这个比较难以解决
    a.insert_info_to_table('film_info', search_film_info_list)




