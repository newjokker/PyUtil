# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import os
from Report.HTHTIssue import HTHTIssue


class MergeUtil(object):

    def __init__(self):
        self.__next_class_info = {'year': 'ji', 'month': 'xun', 'xun': 'day', 'ji': 'month', 'day': None}
        # self.__next_class_info = {'year': 'month', 'month': 'xun', 'xun': 'day', 'ji': 'month', 'day': None}
        # self.__next_class_info = {'year': 'month', 'month': 'day', 'xun': 'day', 'ji': 'month', 'day': None}
        self.__class_info_2 = {'ji': [1, 2, 3, 4], 'year': list(range(1, 13)), 'month': [1, 2, 3]}
        self.assign_issue = None
        self.stop_class = 'xun'  # 截止等级，小于这个等级不进行拆分
        self.file_dir = None

    def get_file_path_by_assign_issue_and_class(self, assign_class, assign_issue:HTHTIssue):
        """根据指定的 issue 找到对应的年的文件的存放位置"""
        # fixme 两种模式，当前指定期次所存在的文件夹路径
        # 日用当天的日期命名
        # 旬，月，季，年 用的是合成的时间命名，就是需要合成的时间范围的最大时间 + 1 个时间段，旬的话用下旬的第一天，月的话，用下个月的第一天
        # fixme 对于不需要精确的部分，使用 0000 来代替，(注意：这样的用法在作为 issue 的时候可能会报错)
        file_dir = ''
        if assign_class == 'year':
            file_dir_year = str(int(assign_issue.get_year_str()) + 1)
            file_dir = os.path.join(self.file_dir, 'year', "{0}01010000".format(file_dir_year))
        elif assign_class == 'ji':
            new_assign_issue = assign_issue.timedelta(months=3)
            file_dir_year = new_assign_issue.get_year_str()
            file_dir_month = str(new_assign_issue.get_ji_month_list()[0]).rjust(2, '0')
            file_dir = os.path.join(self.file_dir, 'ji', "{0}{1}010000".format(file_dir_year, file_dir_month))
        elif assign_class == 'month':
            new_assign_issue = assign_issue.timedelta(months=1)
            file_dir_year = new_assign_issue.get_year_str()
            file_dir_month = new_assign_issue.get_month_str(is_fixed_length=True)
            file_dir = os.path.join(self.file_dir, 'month', "{0}{1}010000".format(file_dir_year, file_dir_month))
        elif assign_class == 'xun':
            new_assign_issue = assign_issue.timedelta(xun=1)
            file_dir_year = new_assign_issue.get_year_str()
            file_dir_month = new_assign_issue.get_month_str(is_fixed_length=True)
            file_dir_day = new_assign_issue.get_day_str(is_fixed_length=True)
            file_dir = os.path.join(self.file_dir, 'xun', "{0}{1}{2}0000".format(file_dir_year, file_dir_month, file_dir_day))
        elif assign_class == 'day':
            file_dir_year = assign_issue.get_year_str()
            file_dir_month = assign_issue.get_month_str(is_fixed_length=True)
            file_dir_day = assign_issue.get_day_str(is_fixed_length=True)
            file_dir = os.path.join(self.file_dir, 'day', "{0}{1}{2}0000".format(file_dir_year, file_dir_month, file_dir_day))
        else:
            raise TypeError('assign class : {0}'.format(assign_class))
        return os.path.join(file_dir, 'test.txt')

    def get_assign_class_issue_list(self, class_1, class_2, issue):
        """任意输入两个级别，输出他们的对应关系，这个应该是在之前写好的"""
        res_issue_list = []
        if class_1 == 'year' and class_2 == 'ji':
            for month_str in ['01', '04', '07', '10']:
                each_issue = HTHTIssue("{0}{1}010000".format(issue.get_year_str(), month_str))
                res_issue_list.append(each_issue)
        elif class_1 == 'year' and class_2 == 'month':
            for month_index in range(1, 13):
                each_issue = HTHTIssue("{0}{1}010000".format(issue.get_year_str(), str(month_index).rjust(2, '0')))
                res_issue_list.append(each_issue)
        elif class_1 == 'year' and class_2 == 'xun':
            pass
        elif class_1 == 'year' and class_2 == 'day':
            pass
        elif class_1 == 'ji' and class_2 == 'month':
            ji_index = issue.get_ji_index()
            month_indexs = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]][ji_index]
            for month_index in month_indexs:
                each_issue = HTHTIssue("{0}{1}010000".format(issue.get_year_str(), str(month_index).rjust(2, '0')))
                res_issue_list.append(each_issue)
        elif class_1 == 'ji' and class_2 == 'xun':
            pass
        elif class_1 == 'ji' and class_2 == 'day':
            pass
        elif class_1 == 'month' and class_2 == 'xun':
            # 指定当前旬的第一天作为旬的 issue
            for day_str in ['01', '11', '21']:
                each_issue = HTHTIssue("{0}{1}{2}0000".format(issue.get_year_str(),
                                                              issue.get_month_str(is_fixed_length=True), day_str))
                res_issue_list.append(each_issue)
        elif class_1 == 'month' and class_2 == 'day':
            for day_index in range(1, issue.get_day_num_in_assign_month(issue.get_year_str(), issue.get_month_str()) + 1):
                each_issue = HTHTIssue("{0}{1}{2}0000".format(issue.get_year_str(),
                                                              issue.get_month_str(is_fixed_length=True),
                                                              str(day_index).rjust(2, '0')))
                res_issue_list.append(each_issue)
        elif class_1 == 'xun' and class_2 == 'day':
            for each_day in issue.get_xun_day_list():
                each_issue = HTHTIssue("{0}{1}{2}0000".format(issue.get_year_str(),
                                                              issue.get_month_str(is_fixed_length=True),
                                                              str(each_day).rjust(2, '0')))
                res_issue_list.append(each_issue)
        else:
            print(class_1, class_2)
            raise ValueError('输入数据有误')
        return res_issue_list

    def do_merge_with_assign_file_list(self, file_list, merge_file_path):
        """对指定的数据列表进行合成"""
        # print("merge file list : {0}".format(file_list))
        # 就是在指定文件夹下面生成需要的文件
        dir_path = os.path.dirname(merge_file_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        # 生成文件
        with open(merge_file_path, 'w') as txt_file:
            txt_file.write('test\n')

    def do_for_product(self, file_path):
        """生产产品"""
        file_dir = os.path.dirname(file_path)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        with open(file_path, 'w') as txt_file:
            txt_file.write('test.txt')
        print("生产产品 ： {0}".format(file_path))

    def check_data_for_merge(self, assign_class, assign_issue):
        """找到合成需要的数据"""
        # todo 数据准备好了就及时进行合成，或者显示缺少数据
        # todo 广度遍历的方式用于寻找是否缺数据
        # todo 深度遍历的方式用于合成数据
        # 遍历得到所有的子项
        loop_info = [{'assign_class': assign_class, 'assign_issue_list': [assign_issue]}]
        # 缺少的最低级别的数据
        lose_file_list = []
        # 需要另外合成的数据
        need_file_list_for_other_merge = []
        # 需要进行合成的数据字典，不缺数据之后，从小到大进行合成
        merge_info = []

        while True:
            # print('-' * 100)
            if len(loop_info) < 1:
                break
            #
            info = loop_info.copy()
            loop_info = []
            for each_info in info:
                class_1 = each_info['assign_class']
                class_2 = self.__next_class_info[class_1]
                for each_issue in each_info['assign_issue_list']:
                    res_issue_list = self.get_assign_class_issue_list(class_1, class_2, each_issue)
                    temp_issue_list = []
                    touch_off_merge = True  # 是否触发合成
                    file_for_merge_list_temp = []
                    for each_res_issue in res_issue_list:
                        file_path = self.get_file_path_by_assign_issue_and_class(class_2, each_res_issue)
                        if os.path.exists(file_path):
                            # print('use  file : {0} : {1}'.format(class_2, file_path))
                            file_for_merge_list_temp.append(file_path)
                        else:
                            touch_off_merge = False
                            # print('need file : {0} : {1}'.format(class_2, file_path))
                            need_file_list_for_other_merge.append(file_path)
                            # 文件不存在就找下一个级别, 看当前级别还有没有下一个级别
                            if class_2 != self.stop_class:
                                temp_issue_list.append(each_res_issue)
                            else:
                                lose_file_list.append(file_path)
                                # 生产对应的产品
                                # self.do_for_product(file_path)
                                raise ValueError('lose product file : {0}'.format(file_path))
                                # fixme 对于丢失数据的处理方式，可以是报错，或者是忽略最基本的数据（存在于忽略列表中的忽略等等）
                    loop_info.append({'assign_class': class_2, 'assign_issue_list': temp_issue_list})
                    if touch_off_merge:
                        # print("merge : {0}".format(file_for_merge_list_temp))
                        # merge_info.append({"class": file_for_merge_list_temp})
                        merge_info.append({"class": class_1, 'file_list': file_for_merge_list_temp, 'issue': each_issue})
                        # print('-'*50)
        return need_file_list_for_other_merge, merge_info, lose_file_list

    def do_merge(self, assign_class, assign_issue):
        """合成"""

        while True:
            need_file_list, merge_info, lose_file_list = a.check_data_for_merge(assign_class, assign_issue)
            if len(need_file_list) == 0:
                print('do merge，退出')
                each_merge_info = merge_info[0]
                merge_class = each_merge_info['class']
                merge_file_list = each_merge_info['file_list']
                merge_issue = each_merge_info['issue']
                # 找到合成后的文件名
                merge_res_file_path = self.get_file_path_by_assign_issue_and_class(merge_class, merge_issue)
                # 合成
                self.do_merge_with_assign_file_list(merge_file_list, merge_res_file_path)
                break
            else:
                if len(merge_info) == 0:
                    for each_file in lose_file_list:
                        print('lose file : {0}'.format(each_file))
                    print('存在需要合并得到的数据，但是找不到对应的文件')
                    break

                for each_merge_info in merge_info:
                    merge_class = each_merge_info['class']
                    merge_file_list = each_merge_info['file_list']
                    merge_issue = each_merge_info['issue']
                    # 找到合成后的文件名
                    merge_res_file_path = self.get_file_path_by_assign_issue_and_class(merge_class, merge_issue)
                    # 合成
                    self.do_merge_with_assign_file_list(merge_file_list, merge_res_file_path)
                    print('do other merge : {0}'.format(each_merge_info))


if __name__ == '__main__':

    # todo 这边增加根据 class 和 issue 去寻找对应文件的功能，找到这个文件返回 True
    # todo 找不到文件可以触发两种可能，重新生成需要的文件，或者直接忽略
    # todo 如果找到全部的文件就触发合并，没找到文件才去添加 issue 到需要的地方

    a = MergeUtil()
    a.stop_class = 'day'
    a.file_dir = r'C:\Users\Administrator\Desktop\hc'

    # todo 现在的问题是，需要延迟两个周期，但是延迟之前需要对周期进行判断，这个需要改进
    a.do_merge('month', HTHTIssue('201904010000'))


