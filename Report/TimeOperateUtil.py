# -*- coding: utf-8  -*-
# -*- author: jokker -*-

"""时间操作函数"""

import datetime
from dateutil.relativedelta import relativedelta
import calendar
import copy
import time


class TimeOperateUtil(object):
    """时间操作"""

    @staticmethod
    def get_year_day_num(year):
        """得到当前年的天数"""
        if calendar.isleap(year):
            return 366
        else:
            return 365

    @staticmethod
    def get_month_day_num(year, month):
        """获取当前月有多少天"""
        firstDayWeekDay, monthRange = calendar.monthrange(int(year), int(month))
        return monthRange

    @staticmethod
    def get_xun_day_num(year, month, assign_xun):
        """获取指定旬的日期长度，旬要和月进行统一，所以 upper 代表第一旬，down 代表第三旬"""
        # 检查旬格式
        if not isinstance(assign_xun, str):
            raise EOFError('assign_xun can only be str')
        # 第一第二旬长度都是固定的 10 天
        if assign_xun in ('upper', 'middle'):
            return 10
        elif assign_xun == 'down':
            # ----------------------------------------------------
            month_day_length = TimeOperateUtil.get_month_day_num(int(year), int(month))
            return month_day_length - 20

    @staticmethod
    def timedelta(assign_date, days=0, hours=0, minutes=0, seconds=0, years=0, months=0):
        """时间操作，之前的方法不支持年和月，在这个方法中增加对一个的参数"""

        # 计算系统支持的偏移
        assign_date += datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
        # 使用新的偏移量计算
        res_date = assign_date + relativedelta(years=years, months=months)
        return copy.deepcopy(res_date)

    # -------------------------- need perfect ---------------------------------------
    @staticmethod
    def offset_month(assign_month, offset_month):
        """计算月的偏移，返回偏移后的月份"""
        offset_month = assign_month + offset_month
        month = offset_month % 12  # 去掉年循环，得到的偏移量
        # 月的范围是 1 - 12
        if month <= 0:
            month += 12
        return month

    @staticmethod
    def timestamp_to_struct_time(timestamp):
        """时间戳转为格式化的时间"""
        time.mktime(timestamp)

    @staticmethod
    def struct_time_to_timestamp(struct_time):
        """格式化的时间转为时间戳"""
        time.strptime(struct_time)


if __name__ == '__main__':

    date_0 = datetime.datetime.now()

    print(TimeOperateUtil.timedelta(date_0, years=-10, months=-1, hours=1))
    #
    # print date_0 + relativedelta(years=-1, months=3)
    #
    # # print datetime.timedelta(days=1, seconds=12, hours=45)
    #
    # a = TimeOperateUtil.get_xun_day_num(date_0, 2)
    #
    # print TimeOperateUtil.offset_month(1, -1)
    # print TimeOperateUtil.offset_month(12, 5)
    # print TimeOperateUtil.offset_month(8, 3)
