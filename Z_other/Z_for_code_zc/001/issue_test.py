# -*- coding: utf-8  -*-
# -*- author: jokker -*-


from Report.HTHTIssue import HTHTIssue

issue = HTHTIssue('201910100740')

# 根据北京时间计算世界时间
print('北京时 {0} 对应的世界时为 {1}\n'.format(issue.get_issue_str(), issue.timedelta(hours=-8).get_issue_str()))

# 获取年月寻的长度
print("2019 年 10 月 有 {0} 天\n".format(issue.get_day_num_in_assign_month(2019, 10)))
print("2019 年 2 月下旬 有 {0} 天\n".format(issue.get_day_num_in_assign_xun(2019, 2, 'down')))
print("当前 issue ：{0} 为 {1} index 为 {2}\n".format(issue.get_issue_str(), issue.get_xun_str(), issue.get_xun_index()))

# 获取当前期次的上旬上月信息
print("上一旬的相关信息为 : {0}\n".format(issue.get_last_xun_info()))
print("上一月的相关信息为 : {0}\n".format(issue.get_lastt_month_info()))

# 替换字典，这个在出图，出报告经常用到，很多人用的是字符串的切片，或者拼接，这样不安全也难以发现错误
print('issue 表示的是 {0}年{1}月{2}日{3}时{4}分\n'.format(issue.get_year_str(), issue.get_month_str(),
                                                 issue.get_day_str(), issue.get_hour_str(), issue.get_minute_str()))
# 计算时间跨度，常用于计算报告的期次
print('第一期为 201910010000 今天的日报是 {0} 期\n'.format(int(HTHTIssue('201910010000').
                                                    get_time_span_to_assign_issue(issue) / (24 * 60 * 60))))
