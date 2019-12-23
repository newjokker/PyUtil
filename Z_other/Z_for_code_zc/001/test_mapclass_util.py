# -*- coding: utf-8  -*-
# -*- author: jokker -*-


from Report.MapClassUtil import AreaInfoOperation, AreaInfo, parse_map_info

areaXmlPath = r'.\AreaCfg.xml'

areaInfoOperator = parse_map_info(areaXmlPath)

# ---------------------- 节点结构信息和属性信息查询 -----------------------------------------------------

# 找到子节点
city_ids = areaInfoOperator.get_child_node_id('QHS')
print('QHS 的子节点 ： {0}\n'.format(','.join(city_ids)))

# 找到父节点
father_id = areaInfoOperator.get_father_node_id('A00000')
print('A00000 的父节点 ： {0}\n'.format(father_id))

# 找到兄弟节点
brother_id = areaInfoOperator.get_brother_node_id('A00000')
print('A00000 的兄弟节点 ： {0}\n'.format(','.join(brother_id)))

# 获取节点属性，看着麻烦，但是链式表达式其实理解很简单，书写也清晰
print('QHS 的 name 属性值 ： {0}\n'.format(areaInfoOperator.get_node_copy('QHS').get_attr_info('name')))

# 找到所有子节点，包括子节点的子节点
all_region_id = areaInfoOperator.get_all_child_node_id('QHS')
print('QHS 的所有子节点的个数为 ：{0} 分别为： {1}\n'.format(len(all_region_id), ','.join(all_region_id)))

# 找到青海省的所有区
all_qu_region_id = areaInfoOperator.get_all_child_node_id('QHS', lambda x: '区' in x.get_attr_info('name'), scan_all=True)
print('QHS 所有子孙节点中 name 属性中含有 区 的节点的 name 分别为 ：{0}\n'.format(
    ', '.join(list(map(lambda x: areaInfoOperator.get_node_copy(x).get_attr_info('name'), all_qu_region_id)))))

# 找到经纬度在一定范围的区域
all_assign_region_id = areaInfoOperator.get_all_child_node_id('QHS',
        lambda x:  100 < float(x.get_attr_info('lon')) < 101 and 36 < float(x.get_attr_info('lat')) < 37, scan_all=True)

print('QHS 所有子孙节点中 中心经纬度在指定范围的有 ：{0}\n'.format(', '.join(all_assign_region_id)))

# ---------------------- 节点结构信息和属性信息操作 -----------------------------------------------------

# 增删改查，