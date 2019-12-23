# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import datetime
from dateutil.relativedelta import relativedelta
import calendar
import copy
import time


class HTHTIssue(object):
    """for htht issue operation"""

    def __init__(self, issue_str):
        if not isinstance(issue_str, HTHTIssue):
            self.__issue_str = issue_str
        else:
            self.__issue_str = issue_str.get_issue_str()
        self.__issue_date = datetime.datetime.strptime(self.__issue_str, "%Y%m%d%H%M")

    def get_issue_str(self):
        return self.__issue_str

    def get_year_str(self):
        return str(self.__issue_date.year)

    def get_month_str(self, is_fixed_length=False):
        if is_fixed_length:
            return str(self.__issue_date.month).rjust(2, '0')
        return str(self.__issue_date.month)

    def get_xun_str(self):
        """get xun string ==> ['upper', 'middle', 'down']"""
        xun_index = self.get_xun_index()
        return ['upper', 'middle', 'down'][xun_index]

    def get_day_str(self, is_fixed_length=False):
        if is_fixed_length:
            return str(self.__issue_date.day).rjust(2, '0')
        return str(self.__issue_date.day)

    def get_hour_str(self, is_fixed_length=False):
        if is_fixed_length:
            return str(self.__issue_date.hour).rjust(2, '0')
        return str(self.__issue_date.hour)

    def get_minute_str(self, is_fixed_length=False):
        if is_fixed_length:
            return str(self.__issue_date.minute).rjust(2, '0')
        return str(self.__issue_date.minute)

    def get_xun_index(self):
        """get xun index ==> [0, 1, 2]"""
        day_index = int(self.get_day_str())

        if day_index <= 10:
            return 0
        elif 10 < day_index <= 20:
            return 1
        else:
            return 2

    def get_ji_index(self):
        assign_month = self.__issue_date.month
        if 0 < assign_month <= 3:
            return 0
        elif 3 < assign_month <= 6:
            return 1
        elif 6 < assign_month <= 9:
            return 2
        elif 9 < assign_month <= 12:
            return 3

    def get_xun_day_list(self):
        xun_index = self.get_xun_index()
        if xun_index == 0:
            return list(range(1, 11))
        elif xun_index == 1:
            return list(range(11, 21))
        else:
            xun_str = self.get_xun_str()
            return list(range(21, 21 + self.get_day_num_in_assign_xun(self.get_year_str(), self.get_month_str(), xun_str)))

    def get_ji_month_list(self):
        return [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]][self.get_ji_index()]

    def get_year_day_num(self):
        """计算当年有所少天"""
        return self.get_day_num_in_assign_year(self.get_year_str())

    def get_month_day_num(self):
        return self.get_day_num_in_assign_month(self.get_year_str(), self.get_month_str())

    def get_xun_day_num(self):
        return self.get_day_num_in_assign_xun(self.get_year_str(), self.get_month_str(), self.get_xun_str())

    def get_time_span_to_assign_issue(self, assign_issue):
        """compute time span between self and assign issue, return > 0  if assign issue > self, unit is second"""
        if isinstance(assign_issue, HTHTIssue):
            assign_issue = assign_issue.get_issue_str()

        assign_time = datetime.datetime.strptime(assign_issue, "%Y%m%d%H%M")
        t1 = time.mktime(self.__issue_date.timetuple()) * 1000 + self.__issue_date.microsecond / 1000
        t2 = time.mktime(assign_time.timetuple()) * 1000 + assign_time.microsecond / 1000
        return (t2 - t1) / 1000  # unit is second

    def __timedelta_in_xun(self, xun_offist, region_day_str):
        """当前日期偏移指定的旬"""
        def get_day_str(xun_index, day_str):
            """已知当前月的天数，偏移之前的 day_str 求偏移后的 day_str"""
            one_str = day_str.rjust(2, '0')[1]
            if day_str not in ['10', '20', '30', '31']:
                if xun_index == 0:
                    return str(one_str).rjust(2, '0')
                elif xun_index == 1:
                    return '1{0}'.format(str(one_str))
                elif xun_index == 2:
                    return '2{0}'.format(str(one_str))
            elif day_str in ['10', '20', '30']:
                if xun_index == 0:
                    return '10'
                elif xun_index == 1:
                    return '20'
                elif xun_index == 2:
                    return '30'
            elif day_str == '31':
                if xun_index == 0:
                    return '10'
                elif xun_index == 1:
                    return '20'
                elif xun_index == 2:
                    return '31'
        # 计算偏移的整月和偏移的旬
        if xun_offist >= 0:
            month_num, xun_num = divmod(xun_offist, 3)
        else:
            month_num, xun_num = divmod(xun_offist, -3)
            month_num = -month_num
        # 将issue 按照月进行偏移
        issue_date = copy.deepcopy(self.__issue_date)
        self.__issue_date = issue_date + relativedelta(months=month_num)
        self.__issue_str = datetime.datetime.strftime(self.__issue_date, "%Y%m%d%H%M")
        # --------------------------------------- 计算偏移后的年月 -------------------------------------------------
        old_xun_index = self.get_xun_index()
        new_xun_index = (old_xun_index + xun_offist) % 3
        old_month_num = int(self.get_month_str())
        old_year_num = int(self.get_year_str())

        new_year_num = old_year_num
        new_month_num = old_month_num
        if xun_num == 1:
            if old_xun_index == 2 and old_month_num == 12:
                new_month_num = 1
                new_year_num = old_year_num + 1
            elif old_xun_index == 2:
                new_month_num = old_month_num + 1
        elif xun_num == 2:
            if old_month_num == 12 and (old_xun_index == 1 or old_xun_index == 2):
                new_month_num = 1
                new_year_num = old_year_num + 1
            elif old_xun_index == 1 or old_xun_index == 2:
                new_month_num = old_month_num + 1
        elif xun_num == -1:
            if old_xun_index == 0 and old_month_num == 1:
                new_month_num = 12
                new_year_num = old_year_num - 1
            elif old_xun_index == 0:
                new_month_num = old_month_num - 1
        elif xun_num == -2:
            if old_month_num == 1 and (old_xun_index == 0 or old_xun_index == 1):
                new_month_num = 12
                new_year_num = old_year_num - 1
            elif old_xun_index == 0 or old_xun_index == 1:
                new_month_num = old_month_num - 1

        new_month_str = str(new_month_num).rjust(2, '0')
        new_year_str = str(new_year_num)
        # --------------------------------------- 计算偏移后的日 ---------------------------------------------------
        new_day_str = get_day_str(new_xun_index, str(region_day_str))
        if new_xun_index == 2 and int(new_day_str) > self.get_day_num_in_assign_month(new_year_num, new_month_num):
            new_day_str = str(self.get_day_num_in_assign_month(new_year_num, new_month_num))

        # 拼接新 issue
        new_issue = "{0}{1}{2}{3}".format(new_year_str, new_month_str, new_day_str, self.__issue_str[8:])
        self.__issue_str = new_issue
        return HTHTIssue(self.__issue_str)

    def timedelta(self, days=0, hours=0, minutes=0, seconds=0, years=0, months=0, xun=0):
        """
        time arithmetic support [year, month, day, hour, minutes, second]
        月的规则是，下个月和这个月应该是同一天，如果没有这个多天，那就天数往多了取 1.30 ==> 2.28 | 1.31 ==> 4.30
        旬我定的规则是，[1,2,3]* 后面的 * 尽量保持不变，变的话就是往多了去取，和月的规则类似, 1.11 => 1.21 | 1.31 ==> 2.28 | 2.28 ==> 3.8

        # 有个很严重的问题，因为旬的偏移和月年的偏移是计算其他的偏移之后做的偏移，这样会造成一个问题 本来是 31 号
        # 偏移一月之后变为 28 号 再偏移 一旬变为 18 号， 其实应该是变为 20 号，也就是说旬偏移是需要单独提出来的，并且难以保证日期的一致性
        # 上述问题已通过在做旬偏移的时候传入初始 day_str 的方式进行了解决
        """

        # compute timedelta by datetime.timedelta
        issue_date = copy.deepcopy(self.__issue_date)
        issue_date += datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
        # compute timedelta by relativedelta
        res_date = issue_date + relativedelta(years=years, months=months)
        # to issue str
        res_date_str = datetime.datetime.strftime(res_date, "%Y%m%d%H%M")
        res_temp = HTHTIssue(res_date_str)
        #
        if xun == 0:
            return res_temp
        # fixme 旬的偏移是有问题的，旬的偏移应该在 月的偏移后面，而且里面的函数写的也是错的，
        return res_temp.__timedelta_in_xun(xun_offist=xun, region_day_str=self.__issue_date.day)

    @staticmethod
    def get_day_num_in_assign_year(year):
        """get how many days the assign year has"""
        if calendar.isleap(int(year)):
            return 366
        else:
            return 365

    @staticmethod
    def get_day_num_in_assign_month(year, month):
        """get how many days the assign month has ==> int"""
        first_day_week_day, month_range = calendar.monthrange(int(year), int(month))
        return month_range

    @staticmethod
    def get_day_num_in_assign_xun(year, month, assign_xun):
        """get how many days the assign xun has, assign xun should be in ['upper', 'middle', 'down'] ==> int"""
        # type checking
        if not isinstance(assign_xun, str):
            raise TypeError('assign_xun can only be str')
        # upper_xun and middele xun has 10 days
        if assign_xun in ('upper', 'middle'):
            return 10
        elif assign_xun == 'down':
            month_day_length = HTHTIssue.get_day_num_in_assign_month(int(year), int(month))
            return month_day_length - 20

    # -------------------------- to delete -----------------------------------------------

    def get_last_xun_info(self):
        """get last xun infomation ==> dict.key : 'year', 'month', 'xun_index', 'xun_str' """
        day_index = int(self.get_day_str())
        if day_index <= 30:
            offst_day_num = 10  # when assign month has 31 days, offset 11 days
        else:
            offst_day_num = 11

        date_last_xun = self.__issue_date + datetime.timedelta(days=-offst_day_num)
        xun_index_last_xun = [2, 0, 1][self.get_xun_index()]
        xun_str_last_xun = ['upper', 'middle', 'down'][xun_index_last_xun]
        return {'year': str(date_last_xun.year), 'month': str(date_last_xun.month),
                'xun_index': str(xun_index_last_xun), 'xun_str': xun_str_last_xun}

    def get_lastt_month_info(self):
        """get last month infomation ==> dict.key : 'year', 'month'"""
        year = int(self.get_year_str())
        month = int(self.get_month_str())

        if month != 1:
            month -= 1
        else:
            month = 12
            year -= 1
        return {'year': str(year), 'month': str(month)}

    def get_next_xun_info(self):
        """get last xun infomation ==> dict.key : 'year', 'month', 'xun_index', 'xun_str' """
        day_index = int(self.get_day_str())
        xun_day_num = self.get_day_num_in_assign_xun(self.get_year_str(), self.get_month_str(), self.get_xun_str())
        # 是下旬，下旬11天，当前day_str == ‘11’
        if day_index == 21 and xun_day_num == 11:
            offst_day_num = 11  # when assign month has 31 days, offset 11 days
        else:
            offst_day_num = 10

        date_next_xun = self.__issue_date + datetime.timedelta(days=offst_day_num)
        xun_index_next_xun = [1, 2, 0][self.get_xun_index()]
        xun_str_last_xun = ['upper', 'middle', 'down'][xun_index_next_xun]
        return {'year': str(date_next_xun.year), 'month': str(date_next_xun.month),
                'xun_index': str(xun_index_next_xun), 'xun_str': xun_str_last_xun}

    def get_next_month_info(self):
        year = int(self.get_year_str())
        month = int(self.get_month_str())

        if month != 12:
            month += 1
        else:
            month = 1
            year += 1
        return {'year': str(year), 'month': str(month)}


if __name__ == "__main__":

    a = HTHTIssue("201901050740")
    b = a.timedelta(hours=-8)
    print(b.get_issue_str())
