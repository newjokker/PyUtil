# -*- coding: utf-8  -*-
# -*- author: jokker -*-

class Solution:

    def myAtoi(self, str_num):

        str_num = str_num.strip()
        is_negative = False

        if not str_num:
            return 0

        if str_num[0] == '-':
            str_num = str_num[1:]
            is_negative = True
        elif str_num[0] == '+':
            str_num = str_num[1:]
            is_negative = False

        use_num = ''

        for each in str_num:
            if each in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}:
                use_num += each
            else:
                break

        if not use_num:
            return 0

        use_num = int(use_num)

        if use_num > 2 ** 31 - 1 and is_negative == False:
            # 是超过范围的正数
            return 2 ** 31 - 1
        elif use_num > 2 ** 31 and is_negative == True:
            # 超过范围的负数
            return -2 ** 31
        elif is_negative:
            return -use_num
        else:
            return use_num


if __name__ == '__main__':

    a = Solution()
    print(a.myAtoi("+-2"))








