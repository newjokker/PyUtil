# -*- coding: utf-8  -*-
# -*- author: jokker -*-

# 中文数字和阿拉伯数字互转

common_used_numerals_tmp = {'零': 0, '一': 1, '二': 2, '两': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
                            '十': 10, '百': 100, '千': 1000, '万': 10000, '亿': 100000000}
common_used_numerals = {}
for key in common_used_numerals_tmp:
    common_used_numerals[key] = common_used_numerals_tmp[key]


def chinese2digits(uchars_chinese):
    total = 0
    r = 1  # 表示单位：个十百千...
    for i in range(len(uchars_chinese) - 1, -1, -1):
        val = common_used_numerals.get(uchars_chinese[i])
        if val >= 10 and i == 0:  # 应对 十三 十四 十*之类
            if val > r:
                r = val
                total = total + val
            else:
                r = r * val
                # total =total + r * x
        elif val >= 10:
            if val > r:
                r = val
            else:
                r = r * val
        else:
            total = total + r * val
    return total


num_str_start_symbol = ['一', '二', '两', '三', '四', '五', '六', '七', '八', '九', '十']
more_num_str_symbol = ['零', '一', '二', '两', '三', '四', '五', '六', '七', '八', '九', '十', '百', '千', '万', '亿']


def changeChineseNumToArab(oriStr):
    """找到中文字符串，对每一个字符串转为阿拉伯数字，思路没有问题，但是判断中文数字字符串的方法不够严谨"""
    lenStr = len(oriStr)
    aProStr = ''
    if lenStr == 0:
        return aProStr

    hasNumStart = False
    numberStr = ''
    for idx in range(lenStr):
        # fixme 将连续的可被识别为中文数字的字符串认作为中文数字字符串，这样会遇到问题，想办法去优化
        if oriStr[idx] in num_str_start_symbol:
            if not hasNumStart:
                hasNumStart = True
            numberStr += oriStr[idx]
        else:
            if hasNumStart:
                if oriStr[idx] in more_num_str_symbol:
                    numberStr += oriStr[idx]
                    continue
                else:
                    # fixme 在转换的之前再从全局判断一下找到的是否是合法的中文数字字符串
                    print(numberStr)
                    numResult = str(chinese2digits(numberStr))
                    numberStr = ''
                    hasNumStart = False
                    aProStr += numResult
            aProStr += oriStr[idx]

    if len(numberStr) > 0:
        resultNum = chinese2digits(numberStr)
        aProStr += str(resultNum)

    return aProStr


if __name__ == '__main__':


    print(changeChineseNumToArab('你说百十千万都是一百二十个人百姓不知道啊'))