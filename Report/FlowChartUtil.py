# -*- coding: utf-8  -*-
# -*- author: jokker -*-

"""
流程图相关，
（1）参考 markdown 的格式来做流程图
（2）自定义格式来做流程图
"""

#


class FlowChartUtil(object):
    """自动生成流程图"""

    def get_flow_char(self, flow_grade):
        """字典转为结构图, 字典里面套字典的结构"""

        # todo 获取列表的等级关系
        # todo 设置等级关系
        # todo 最后一个级别是列表，其他的级别是字典
        # todo 分为属性信息和等级信息，属性信息

        # todo 使用树结构来记录等级关系

        for each_head in flow_grade:
            # 每一个头
            # 用栈来表示 []
            # 拿到所有的元素，看看有没有重复的，最后一个级别是列表
            while True:
                pass




# from graphviz import Digraph
#
# dot = Digraph(comment='The Test Table', format="png")
#
# # 添加圆点A,A的标签是Dot A
# dot.node('A', 'Dot A')
#
# # 添加圆点 B, B的标签是Dot B
# dot.node('B', 'Dot B')
# dot.node('C', 'Dot C')
#
# for i in range(10):
#     dot.node(str(i), 'Dot {0}'.format(i))
#     for j in range(10):
#         dot.node('{0}_{1}'.format(i,j))
#         dot.edge(str(i), '{0}_{1}'.format(i, j), 'test')
#
#
# # 创建一堆边，即连接AB的两条边，连接AC的一条边。
# dot.edges(['AB'])
# dot.edge('A', 'C', 'test_AC')
#
# # 保存source到文件，并提供Graphviz引擎
# dot.save(r'C:\Users\Administrator\Desktop\del\FlowChartUtil\test-table.gv')  # 保存
# dot.render(r'C:\Users\Administrator\Desktop\del\FlowChartUtil\test-table2.gv')
# # dot.view()  # 显示


if __name__ == "__main__":

    a = {'a': {'b': ['b1', 'b2', 'b3'], 'c': ['c1', 'c2'], 'd': ['d1', 'd2', 'd3', 'd4']}}

    fc = FlowChartUtil()
    fc.get_flow_char(a)

    pass


