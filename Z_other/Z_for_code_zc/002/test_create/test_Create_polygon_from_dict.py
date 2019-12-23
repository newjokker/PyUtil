# -*- coding: utf-8  -*-
# -*- author: jokker -*-


from Report.GdalUtil import CreateOgr

# line_info = [{'points': [(102, 44), (105, 45), (145, 56)], 'hehe':123},
#              {'points': [(103, 4.4), (10.5, 45), (14.5, 56)], 'hehe':123},
#              {'points': [(10, 10), (10, 20), (20, 20), (20, 10)], 'hehe': 123}]

line_info = [{'points': [(101.85, 27.90), (102.38, 27.90), (102.40, 27.48), (101.85, 27.50)]}]

save_path = r'E:\Algorithm\Util_Util\Z_for_code_zc\002\data\factory.shp'

CreateOgr.create_polygon_from_dict(line_info, save_path)


