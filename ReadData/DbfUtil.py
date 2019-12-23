# -*- coding: utf-8  -*-
# -*- author: jokker -*-

from dbfread import DBF


class DbfUtil(object):
    """read dbf file，to replace arcpy --> arcpy.da.SearchCursor"""

    @staticmethod
    def get_table(dbf_path, need_field=None):
        """read dbf file，return dict"""
        result = []
        table = DBF(dbf_path)
        # field to get
        if need_field is None or need_field == "*":
            need_field = table.field_names

        # # 判断字段是否有误
        # for each_need_field in need_field:
        #     if each_need_field not in table.field_names:
        #         raise TypeError('{0} is not in field names'.format(each_need_field))

        # loop for every line
        for each_line in table:
            result_temp = []
            for field in need_field:
                result_temp.append(each_line[field])
            result.append(result_temp)
        return result

    @staticmethod
    def get_title(dbf_path):
        table = DBF(dbf_path)
        return table.field_names


if __name__ == "__main__":

    # import arcpy
    #
    # cursor = arcpy.da.SearchCursor(r'D:\Code\QingHai_73\Depend\QingHai\CompShp\AreaCounty.shp', 'ID')  # 查询需要的字段
    # # cursor = DbfUtil.get_table(out_table, need_data_list)  # 查询需要的字段
    #
    # # 格式化输出
    # for each_line in cursor:
    #     print(each_line)

    # a = DbfUtil.get_table(r'D:\Code\QingHai_73\Depend\QingHai\CompShp\AreaCity.dbf')
    c = DbfUtil.get_table(r'C:\Users\Administrator\Desktop\duanzi.dbf')

    for each in c:
        print(each)

    # print(DbfUtil.get_title(r'C:\Users\74722\Desktop\依赖注入\temp\d59bf.dbf'))
    #
    # a = DbfUtil.get_table(r'C:\Users\74722\Desktop\依赖注入\temp\d59bf.dbf', ['CID', 'RANGE', 'AREA', 'MIN', 'MIN', 'CID'])
    #
    # for each in a:
    #     print(each)
