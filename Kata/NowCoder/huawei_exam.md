# -*- coding: utf-8  -*-
# -*- author: jokker -*-


# 1. 计算字符串最后一个单词的长度，单词以空格隔开。
# import sys
# 
# for line in sys.stdin:  # 读入数据
#     a = line.split()
#     print
#     len(a[-1])

2.写出一个程序，接受一个由字母和数字组成的字符串，和一个字符，然后输出输入字符串中含有该字符的个数。不区分大小写。

a = input().lower()
b = input().lower()
print(a.count(b))
注：Python
lower()
方法转换字符串中所有大写字符为小写。

3.明明想在学校中请一些同学一起做一项问卷调查，为了实验的客观性，他先用计算机生成了N个1到1000之间的随机整数（N≤1000），对于其中重复的数字，只保留一个，把其余相同的数去掉，不同的数对应着不同的学生的学号。然后再把这些数从小到大排序，按照排好的顺序去找同学做调查。请你协助明明完成“去重”与“排序”的工作(
    同一个测试用例里可能会有多组数据，希望大家能正确处理)。

while True:
    try:
        n = int(input())  # 读入第一行：随机整数的个数
        res = set()
        for i in range(n):
            res.add(int(input()))  # 读入第n行：n个随机整数组成的数组 
        for i in sorted(res):
            print(i)
    except:
        break
 注：set是一个无序且不重复的元素集合。

4.• 连续输入字符串，请按长度为8拆分每个字符串后输出到新的字符串数组；
   • 长度不是8整数倍的字符串请在后面补数字0，空字符串不处理。

def printStr(string):
    if len(string) <= 8:
        print(string + "0" * (8 - len(string)))
    else:
        while len(string) > 8:
            print(string[:8])
            string = string[8:]
        print(string + "0" * (8 - len(string)))


a = input()
b = input()
printStr(a)
printStr(b)
 
5.写出一个程序，接受一个十六进制的数值字符串，输出该数值的十进制字符串。（多组同时输入 ）

while True:
    try:
        print(int(input(), 16))
    except:
        break
 python整数之间的进制转换:

10
进制转16进制: hex(16)   == >  0x10
16
进制转10进制: int('0x10', 16)   == >  16

6. 功能: 输入一个正整数，按照从小到大的顺序输出它的所有质数的因子（如180的质数因子为2 2 3 3 5 ）, 最后一个数后面也要有空格

a = int(input())


def q(x):
    iszhi = 1
    for i in range(2, int(x ** 0.5 + 2)):
        if x % i == 0:
            iszhi = 0
            print(str(i), end=" ")
            q(int(x / i))
            break
    if iszhi == 1:
        print(str(x), end=" ")


q(a)
注：质数（prime
number）又称素数。质数定义为在大于1的自然数中，除了1和它本身以外不再有其他因数的数称为质数

7.写出一个程序，接受一个正浮点数值，输出该数值的近似整数值。如果小数点后数值大于等于5, 向上取整；小于5，则向下取整。

print(round(float(input()) + 0.001))
注：由于python对于浮点数存储有点抽风（4.5
会存储成4
.4999999），所以要加上0
.001

8. 数据表记录包含表索引和数值，请对表索引相同的记录进行合并，即将相同索引的数值进行求和运算，输出按照key值升序进行输出。

from collections import defaultdict

while True:
    try:
        a = int(input())
        dd = defaultdict(int)  # 指定字典的值为int
        for i in range(a):
            key, val = map(int, input().split())
            dd[key] += val
        for i in sorted(dd.keys()):
            print(str(i) + " " + str(dd[i]))
    except:
        break
 defaultdic默认字典, 使用defaultdict任何未定义的key都会默认返回一个根据method_factory参数不同的默认值, 而相同情况下dict()
会返回KeyError.

9. 输入一个int型整数，按照从右向左的阅读顺序，返回一个不含重复数字的新的整数。

result = ""
for i in input()[::-1]:
    if i not in result:
        result += i
print(result)

10. 编写一个函数，计算字符串中含有的不同字符的个数。字符在ACSII码范围内(0~127)。不在范围内的不作统计。

print(len(set([i for i in input() if ord(i) in range(128)])))
import sys

print(len(set(list(sys.stdin.readline()))))

11. 输入一个整数，将这个整数以字符串的形式逆序输出, 程序不考虑负数的情况，若数字含有0，则逆序形式也含有0，如输入为100，则输出为001

print(input()[::-1])
line = "abcde"
line[:-1]
结果为：'abcd'
其实就是去除了这行文本的最后一个字符（换行符）后剩下的部分。
line = "abcde"
line[::-1]
结果为：'edcba'
倒序输出

12. 写出一个程序，接受一个字符串，然后输出该字符串反转后的字符串。例如：abcd - --------dcba

print(input()[::-1])

13. 将一个英文语句以单词为单位逆序排放。例如“I am a boy”，逆序排放后为“boy a am I”所有单词之间用一个空格隔开，语句中除了英文字母外，不再包含其他字符

print(" ".join(input().split()[::-1]))

14. 给定n个字符串，请对n个字符串按照字典序排列。

num = int(input())
s = []
for i in range(num):
    s.append(input())
s.sort()
for i in s:
    print(i)
注：sort功能很强大
无论是字母或者数字都可以排序

15. 输入一个int型的正整数，计算出该int型数据在内存中存储时1的个数。

a = int(input())
print(bin(a).replace("0b", "").count("1"))

16. 求最小公倍数

正整数A和正整数B 的最小公倍数是指 能被A和B整除的最小的正整数值，设计一个算法，求输入A和B的最小公倍数。

def gcd(a, b):
    """最大公约数."""
    while b:
        a, b = b, a % b
    return a


def lcm(a, b):
    """最小公倍数."""
    return a * b // gcd(a, b)  # //表示整数除法


while True:
    try:
        a, b = map(int, input().split())
        print(lcm(a, b))
    except:
        break
最大公因数的算法：

(1)
辗转相除法：有两整数a和b：

① a % b得余数c

② 若c = 0，则b即为两数的最大公约数

③ 若c≠0，则a = b，b = c，再回去执行①

map接收一个函数和一个可迭代对象（如列表）作为参数，用函数处理每个元素，然后返回新的列表。　　

ACM有时需要要a
b
c这样的一行格式输入，这时可以用map函数来处理，这里假设a, b, c都是整数。

例如：a, b, c = map(int, raw_input().split())

17. 计算一个数字的立方根，不使用库函数

# 牛顿迭代
a = float(input())
e = 0.0001
t = a
while abs(t * t * t - a) > e:
    # x(i+1) = x(i) - f(xi)/f(xi)'
    t = t - (t * t * t - a) * 1.0 / (3 * t * t)
print("%.1f" % t)

18. 将一个字符串str的内容颠倒过来，并输出。str的长度不超过100个字符。 如：输入“I am a student”，输出“tneduts a ma I”。

print(input()[::-1])

19. 从输入任意个整型数，统计其中的负数个数并求所有非负数的平均值

a = input().split()
fu = []
zheng = []
for i in a:
    if int(i) < 0:
        fu.append(int(i))
    else:
        zheng.append(int(i))
print(len(fu))
print(round(sum(zheng) / len(zheng), 1))
 注：最后四舍五入保留一位小数，round(n, 1)

20. Redraiment是走梅花桩的高手。Redraiment总是起点不限，从前到后，往高的桩子走，但走的步数最多，不知道为什么？你能替Redraiment研究他最多走的步数吗

# 最长上升子序列
import bisect

while True:
    try:
        a, b = int(input()), map(int, input().split())
        q = []
        for v in b:
            pos = bisect.bisect_left(q, v)
            if pos == len(q):
                q.append(v)
            else:
                q[pos] = v
        print(len(q))

    except:
        break
注：动态规划之最长上升子序列。

21. 输入一个字符串，对字符中的各个英文字符，数字，空格进行统计（可反复调用）
按照统计个数由多到少输出统计结果，如果统计的个数相同，则按照ASII码由小到大排序输出

while True:
    try:
        from collections import defaultdict

        dd, s, res = defaultdict(list), input(), ""
        for i in set(s):
            dd[s.count(i)].append(i)
        for i in sorted(dd.keys(), reverse=True):
            res += "".join(sorted(dd[i], key=ord))
        print(res)

    except:
        break
22. 输入整型数组和排序标识，对其元素按照升序或降序进行排序（一组测试用例可能会有多组数据）

while True:
    try:
        a = int(input())
        b = map(int, input().split())
        c = int(input())
        if c == 0:
            print(" ".join(map(str, sorted(b, reverse=False))))
        if c == 1:
            print(" ".join(map(str, sorted(b, reverse=True))))
    except:
        break
23. 功能: 等差数列 2，5，8，11，14。。。。

输入: 正整数N  > 0

输出: 求等差数列前N项和

while True:
    try:
        a = int(input())
        print(3 * a * (a - 1) // 2 + 2 * a)
    except:
        break
注：等差数列求和公式：Sn = a1 * n + n * (n - 1) * d / 2

24. 自守数是指一个数的平方的尾数等于该数自身的自然数。例如：25 ^ 2 = 625，76 ^ 2 = 5776，9376 ^ 2 = 87909376。请求出n以内的自守数的个数

while True:
    try:
        a, res = int(input()), 0
        for i in range(0, a + 1):
            if str(i ** 2).endswith(str(i)):
                res += 1
        print(res)
    except:
        break
 注：Python
endswith()
方法用于判断字符串是否以指定后缀结尾，如果以指定后缀结尾返回True，否则返回False。可选参数
"start"
与
"end"
为检索字符串的开始与结束位置。

26. 首先输入要输入的整数个数n，然后输入n个整数。输出为n个整数中负数的个数，和所有正整数的平均值，结果保留一位小数。

while True:
    try:
        a, nums, pos, neg = int(input()), map(int, input().split()), [], 0
        for num in nums:
            if num > 0:
                pos.append(num)
            elif num < 0:
                neg += 1
        print(str(neg) + " 0" if not pos else str(neg) + " " + "{0:.1f}".format(sum(pos) / len(pos)))

    except:
        break

27. 将一个字符中所有出现的数字前后加上符号“ * ”，其他字符保持不变

while True:
    try:
        a, res, isNum = input(), "", False
        for i in a:

            if i.isdigit():
                if not isNum:
                    res = res + "*" + i
                else:
                    res += i
                isNum = True
            else:
                if isNum:
                    res = res + "*" + i
                else:
                    res += i
                isNum = False
        if a[-1].isdigit():
            res += "*"
        print(res)


    except:
        break
 

29. 计票统计

输入：候选人的人数，第二行输入候选人的名字，第三行输入投票人的人数，第四行输入投票。

输出：每行输出候选人的名字和得票数量。

from collections import Counter

while True:
    try:
        a = input()
        b = input().split()
        c = input()
        d = input().split()
        invalid = 0
        cc = Counter(d)
        for i in b:
            print(i + " : " + str(cc[i]))
            invalid += cc[i]
        print("Invalid : " + str(len(d) - invalid))
    except:
        break
 

30. 编写一个函数，传入一个int型数组，返回该数组能否分成两组，使得两组中各元素加起来的和相等，并且，所有5的倍数必须在其中一个组中，所有3的倍数在另一个组中（不包括5的倍数），能满足以上条件，返回true；不满足时返回false。

while 1:
    try:
        n = raw_input()
        l = raw_input().split()
        sum1 = sum2 = 0
        ll = []
        for i in l:
            if int(i) % 5 == 0:
                sum1 += int(i)
            elif int(i) % 3 == 0:
                sum2 += int(i)
            else:
                ll.append(int(i))
        d_value = abs(sum1 - sum2)
        if not ll and d_value == 0:
            print
            'true'
        elif not ll and d_value != 0:
            print
            'false'
        else:
            s = set()
            for x in ll:
                tmp = list(s)
                for y in tmp:
                    s.add(x + y)
                s.add(x)
            for may_value in s:
                if d_value == abs((sum(ll) - may_value) - may_value):
                    print
                    'true'
                    break
            else:
                print
                'false'
    except:

31. 在字符串中找出连续最长的数字字符串。

输入：一个字符串。

输出：字符串中最长的数字字符串和它的长度。如果有相同长度的串，则要一块儿输出，但是长度还是一串的长度

while True:
    try:
        a = input()
        maxLen, maxStrs, curLen, curStr = 0, [], 0, ""
        for i, v in enumerate(a):
            if v.isnumeric():
                curLen += 1
                curStr += v
                if curLen > maxLen:
                    maxLen = curLen
                    maxStrs = [curStr]
                elif curLen == maxLen:
                    maxStrs.append(curStr)
            else:
                curLen = 0
                curStr = ""
        print("".join(maxStrs) + "," + str(maxLen))
    except:
        break
 

 

37. 功能: 求一个byte数字对应的二进制数字中1的最大连续数，例如3的二进制为00000011，最大连续2个1

while True:
    try:
        res, a = 0, bin(int(input())).replace("0b", "")
        for i in range(1, len(a) + 1):
            if "1" * i in a:
                res = i
            else:
                break
        print(res)
    except:
        break
 

39. 找出给定字符串中大写字符(即
'A' - 'Z')的个数

import sys

for a in sys.stdin:
    count = 0
    for i in a:
        if i.isupper():
            count += 1
    print(count)
 

41. 字符串匹配：判断短字符串中的所有字符是否在长字符串中全部出现

while True:
    try:
        a, b = set(input()), set(input())
        print("true" if a & b == a else "false")
    except:
        break

42. 将两个整型数组按照升序合并，并且过滤掉重复数组元素

while True:
    try:
        a, b, c, d = input(), list(map(int, input().split())), input(), list(map(int, input().split()))
        print("".join(map(str, sorted(list(set(b + d))))))

    except:
        break

43. 计算字符串的相似度


def editDistance(str1, str2):
    len1, len2 = len(str1) + 1, len(str2) + 1
    dp = [[0 for i in range(len2)] for j in range(len1)]
    for i in range(len1):
        dp[i][0] = i
    for j in range(len2):
        dp[0][j] = j
    for i in range(1, len1):
        for j in range(1, len2):
            dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + (str1[i - 1] != str2[j - 1]))
    return dp[-1][-1]


while True:
    try:
        print("1/" + str(editDistance(input(), input()) + 1))
    except:
        break

44. 请设计一个算法完成两个超长正整数的加法。

while True:
    try:
        a = input()
        b = input()
        print(str(int(a) + int(b)))
    except:
        break
 

45. 计算两个字符串的最大公共字串的长度，字符不区分大小写


def find_lcsubstr(s1, s2):
    m = [[0 for i in range(len(s2) + 1)] for j in range(len(s1) + 1)]  # 生成0矩阵，为方便后续计算，比字符串长度多了一列 
    mmax = 0  # 最长匹配的长度 
    p = 0  # 最长匹配对应在s1中的最后一位 
    for i in range(len(s1)):
        for j in range(len(s2)):
            if s1[i] == s2[j]:
                m[i + 1][j + 1] = m[i][j] + 1
                if m[i + 1][j + 1] > mmax:
                    mmax = m[i + 1][j + 1]
                    p = i + 1
    return mmax  # 返回最长子串及其长度 


while True:
    try:
        a, b = input(), input()
        print(find_lcsubstr(a, b))
    except:
        break
 

51. 实现删除字符串中出现次数最少的字符，若多个字符出现次数一样，则都删除。输出删除这些单词后的字符串，字符串中其它字符保持原来的顺序。

from collections import defaultdict

while True:
    try:
        a = input()
        dd = defaultdict(int)
        for i in a:
            dd[i] += 1
        for i in dd:
            if dd[i] == min(dd.values()):
                a = a.replace(i, "")
        print(a)
    except:
        break
注：Python
字典(Dictionary)
values()
函数以列表返回字典中的所有值。

52. 中级对字符串中的所有单词进行倒排。（非构成单词的字符均视为单词间隔符）


s = input()
for i in s:
    if not i.isalnum():
        s = s.replace(i, ' ')
s = s.split()
s.reverse()
new_s = ' '.join(s)
print(new_s)
注：Python
isalnum()
方法检测字符串是否由字母和数字组成。

list.reverse()
函数用于反向列表中元素。

53. 输出7有关数字的个数，包括7的倍数，还有包含7的数字（如17，27，37..
.70，71，72，73...）的个数（一组测试用例里可能有多组数据，请注意处理）

while True:
    try:
        a = int(input())
        res = 0
        for i in range(7, a + 1):  # 右边是开区间
            if "7" in str(i) or i % 7 == 0:
                res += 1
        print(res)
    except:
        break

54. 输入n个整数，输出其中最小的k个。

输入说明 
1 输入两个整数 
2 输入一个整数数组
while True:
    try:
        count = int(input().split()[1])
        array = list(map(int, input().strip().split()))
        print(" ".join(map(str, sorted(array)[:count])))
    except:
        break
 注：Python
strip()
方法用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列。

55. 找出字符串中第一个只出现一次的字符（通过率30 %）

while True:
    try:
        s = input()
        for i in s:
            if s.count(i) == 1:
                print(i)
                break
            else:
                print(-1)
    except:
        break
while True:
    try:
        from collections import Counter

        a = input()
        c = list(map(lambda c: c[0], list(filter(lambda c: c[1] == 1, Counter(a).most_common()))))
        if not c: print(-1)
        for i in a:
            if i in c:
                print(i)
                break

    except:
        break
 

56. 任意一个偶数（大于2）都可以由2个素数组成，组成偶数的2个素数有很多种情况，本题目要求输出组成指定偶数的两个素数差值最小的素数对

import math


def isPrime(n):
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


while True:
    try:
        num, start = int(input()) // 2, 1
        if num % 2 == 1:
            start = 0
        for i in range(start, num, 2):
            a, b = num + i, num - i
            if isPrime(a) and isPrime(b):
                print(b)
                print(a)
                break

    except:
        break
57. 输入一个整数, 计算整数二进制中1的个数

while True:
    try:
        a = int(input())
        print(bin(a).count("1"))
    except:
        break
注：当出现错误时，添加while
true  try except试试

58. 一个DNA序列由A / C / G / T四个字母的排列组合组成。G和C的比例（定义为GC - Ratio）是序列中G和C两个字母的总的出现次数除以总的字母数目（也就是序列长度）。在基因工程中，这个比例非常重要。因为高的GC - Ratio可能是基因的起始点。

给定一个很长的DNA序列，以及要求的最小子序列长度，研究人员经常会需要在其中找出GC - Ratio最高的子序列。

while True:
    try:
        a, b = input(), int(input())
        maxStr, maxCnt = a[:b], a[:b].count("C") + a[:b].count("G")
        for i in range(0, len(a) - b):
            if a[i:i + b].count("C") + a[i:i + b].count("G") > maxCnt:
                maxCnt = a[i:i + b].count("C") + a[i:i + b].count("G")
                maxStr = a[i:i + b]
        print(maxStr)
    except:
        break

59. 输入一行字符，分别统计出包含英文字母、空格、数字和其它字符的个数。

while True:
    try:
        a = input()
        char, space, number, other = 0, 0, 0, 0
        for i in a:
            if i == " ":
                space += 1
            elif i.isnumeric():
                number += 1
            elif i.isalpha():
                char += 1
            else:
                other += 1
        print(char)
        print(space)
        print(number)
        print(other)
    except:
        break

60. 字符串排序

while True:
    try:
        a = input()
        # res是最终返回的字符串的列表形式，char是提取的英文字母。
        res, char = [False] * len(a), []
        # 经过这个循环，把相应的非英文字母及其位置存储到了res中。并且把英文字母提取出来了。
        for i, v in enumerate(a):
            if v.isalpha():
                char.append(v)
            else:
                res[i] = v
        # 使用lambda表达式排序，暴力有效。
        char.sort(key=lambda c: c.lower())
        # 将char中对应的字符填到res中。
        for i, v in enumerate(res):
            if not v:
                res[i] = char[0]
                char.pop(0)
        print("".join(res))
    except:
        break

61. 有一只兔子，从出生后第3个月起每个月都生一只兔子，小兔子长到第三个月后每个月又生一只兔子，假如兔子都不死，问每个月的兔子总数为多少？

# 第一个月一只，第二个月一只，第三个月两只。然后符合且波纳契数列
while True:
    try:
        a = int(input())
        arr = [1, 1]
        while len(arr) < a:
            arr.append(arr[-1] + arr[-2])
        print(arr[-1])
    except:
        break

62. 有这样一道智力题：“某商店规定：三个空汽水瓶可以换一瓶汽水。小张手上有十个空汽水瓶，她最多可以换多少瓶汽水喝？”答案是5瓶，方法如下：先用9个空瓶子换3瓶汽水，喝掉3瓶满的，喝完以后4个空瓶子，用3个再换一瓶，喝掉这瓶满的，这时候剩2个空瓶子。然后你让老板先借给你一瓶汽水，喝掉这瓶满的，喝完以后用3个空瓶子换一瓶满的还给老板。如果小张手上有n个空汽水瓶，最多可以换多少瓶汽水喝？

while True:
    try:
        a = int(input())
        if a != 0:
            print(a // 2)

    except:
        break
注：通过数学分析，最后获得的饮料数是总空瓶数整除2 。

 

63. 密码验证合格:

1.
长度超过8位

2.
包括大小写字母.数字.其它符号, 以上四种至少三种

3.
不能有相同长度超2的子串重复

import re
import sys

for i in sys.stdin.readlines():
    print
    "OK" if len(i.strip()) > 8 and sum(
        [1 if re.search(r"[A-Z]", i.strip()) else 0, 1 if re.search(r"[a-z]", i.strip()) else 0,
         1 if re.search(r"[0-9]", i.strip()) else 0, 1 if re.search(r"[^0-9a-zA-Z]", i.strip()) else 0]) > 2 and sum(
        map(lambda c: i.strip().count(i.strip()[c:c + 3]) > 1, range(1, len(i.strip()) - 3))) == 0 else "NG"
注： re.findall
的简单用法（返回string中所有与pattern相匹配的全部字串，返回形式为数组）

 
findall(pattern, string, flags=0)

64. 简单密码破解

他是这么变换的，大家都知道手机上的字母： 1 - -1， abc - -2, 

def --3,

 ghi - -4, jkl - -5, mno - -6, pqrs - -7, tuv - -8 wxyz - -9, 0 - -0, 就这么简单，渊子把密码中出现的小写字母都变成对应的数字，数字和其他的符号都不做变换，


d = {
    "abc": 2,
    "def": 3,
    "ghi": 4,
    "jkl": 5,
    "mno": 6,
    "pqrs": 7,
    "tuv": 8,
    "wxyz": 9,

}
while True:
    try:
        a, res = input(), ""
        for i in a:
            if i.isupper():
                if i != "Z":
                    res += chr(ord(i.lower()) + 1)
                else:
                    res += "a"
            elif i.islower():
                for j in d.keys():
                    if i in j:
                        res += str(d[j])
                        break
            else:
                res += i
        print(res)

    except:
        break

65. 计算最少出列多少位同学，使得剩下的同学排成合唱队形

算法：动态规划
用到概念：递增子序列


# -*- coding:utf-8 -*-
def middle(b, target):  # b为排序数组，所以能进行二分查找，pos返回当前的target在b数组中是第几大的数，也就是前面有多少是有序的
    low = 0
    high = len(b) - 1
    pos = len(b)
    while (low < high):
        mid = (low + high) / 2
        if (b[mid] < target):
            low = mid + 1
        else:
            high = mid
            pos = high
    return pos


def deal(array, res):
    b = [9999] * len(array)
    b[0] = array[0]
    res = res + [1]
    for i in range(1, len(array)):
        pos = middle(b, array[i])
        res = res + [pos + 1]  # 前面有几个比当前数小的值
        b[pos] = array[i]  # 让数组b有序，且每个位置上的数都变成遍历到的最小值
    return res


while True:
    try:
        n = int(raw_input())
        a = raw_input().split(' ')
        array = map(int, a)
        dp1 = []
        dp2 = []
        dp1 = deal(array, dp1)
        array.reverse()
        dp2 = deal(array, dp2)
        dp2.reverse()
        a = max(dp1[i] + dp2[i] for i in range(n))
        print(n - a + 1)
    except:
        break

66. 请解析IP地址和对应的掩码，进行分类识别。要求按照A / B / C / D / E类地址归类，不合法的地址和掩码单独归类。

输入：多行字符串。每行一个IP地址和掩码，用
~隔开。

输出: 统计A、B、C、D、E、错误IP地址或错误掩码、私有IP的个数，之间以空格隔开。


# -*- coding: utf-8 -*-

import re


def isLegalIP(IP):
    if not IP or IP == "":
        return False

    pattern = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
    match = pattern.match(IP)
    if not match:
        return False

    nums = IP.split(".")
    for num in nums:
        n = int(num)
        if n < 0 or n > 255:
            return False

    return True


def CatagoryIP(IP):
    if not IP or IP == "":
        return False
    nums = IP.split(".")
    # A
    if 126 >= int(nums[0]) >= 1:
        return "A"
    # B
    if 191 >= int(nums[0]) >= 128:
        return "B"
    # C
    if 223 >= int(nums[0]) >= 192:
        return "C"
    # D
    if 239 >= int(nums[0]) >= 224:
        return "D"
    # E
    if 255 >= int(nums[0]) >= 240:
        return "E"

    return False


def isPrivateIP(IP):
    if not IP or IP == "":
        return False

    nums = IP.split(".")
    if int(nums[0]) == 10:
        return True
    if int(nums[0]) == 172:
        if 31 >= int(nums[1]) >= 16:
            return True
    if int(nums[0]) == 192 and int(nums[1]) == 168:
        return True

    return False


def isLegalMaskCode(Mask):
    if not Mask or Mask == "":
        return False
    if not isLegalIP(Mask):
        return False

    binaryMask = "".join(map(lambda x: bin(int(x))[2:].zfill(8), Mask.split(".")))
    indexOfFirstZero = binaryMask.find("0")
    indexOfLastOne = binaryMask.rfind("1")
    if indexOfLastOne > indexOfFirstZero:
        return False
    return True


try:
    A, B, C, D, E, Err, P = [0, 0, 0, 0, 0, 0, 0]
    while True:
        s = raw_input()
        IP, Mask = s.split("~")

        if not isLegalIP(IP) or not isLegalMaskCode(Mask):
            Err += 1
        else:
            if isPrivateIP(IP):
                P += 1
            cat = CatagoryIP(IP)
            if cat == "A":
                A += 1
            if cat == "B":
                B += 1
            if cat == "C":
                C += 1
            if cat == "D":
                D += 1
            if cat == "E":
                E += 1

except:
    print(A, B, C, D, E, Err, P)
    pass
 

67. 蛇形矩阵

while True:
    try:
        n, curNum = int(input()), 1
        res = [[0 for i in range(n)] for j in range(n)]
        for i in range(n):
            for j in range(i + 1):
                res[i - j][j] = curNum
                curNum += 1
        for i in res:
            print(" ".join(map(str, (filter(lambda i: i != 0, i)))))
    except:
        break

68. 购物车


def max_fun(N, m, v, p, q):
    res = [[0] * (N + 1) for _ in range(m + 1)]
    # 商品
    for i in range(1, m + 1):
        # 价格
        for j in range(10, N + 1, 10):
            # 为主件时
            if q[i - 1] == 0:  # 主件
                # res[i][j]= res[i-1][j]
                if v[i - 1] <= j:
                    res[i][j] = max(res[i - 1][j], res[i - 1][j - v[i - 1]] + v[i - 1] * p[i - 1])
            # 为配件时  q[i-1] != 0
            elif v[i - 1] + v[q[i - 1]] <= j:
                res[i][j] = max(res[i - 1][j],
                                res[i - 1][j - v[i - 1] - v[q[i - 1]]] + v[i - 1] * p[i - 1] + v[q[i - 1]] * p[
                                    q[i - 1]])
    print(res[m][int(N / 10) * 10])


N_m = input().split(' ')
N = int(N_m[0])
m = int(N_m[1])
v = []
p = []
q = []
for i in range(m):
    vpq = input().split(' ')
    v.append(int(vpq[0]))
    p.append(int(vpq[1]))
    q.append(int(vpq[2]))
max_fun(N, m, v, p, q)

69. 输入一个字符串, 输出: 返回有效密码串的最大长度(密码是对称的)


def longestPalindrome(s):
    if s == s[::-1]: return len(s)
    maxLen = 0
    for i in range(len(s)):
        if i - maxLen >= 1 and s[i - maxLen - 1:i + 1] == s[i - maxLen - 1:i + 1][::-1]:
            maxLen += 2
            continue
        if i - maxLen >= 0 and s[i - maxLen:i + 1] == s[i - maxLen:i + 1][::-1]:
            maxLen += 1
    return maxLen


while True:
    try:
        a = input()
        if a:
            print(longestPalindrome(a))

    except:
        break
        
        
70. 名字的漂亮程度：给出一个名字，该名字有26个字符串组成，定义这个字符串的“漂亮度”是其所有字母“漂亮度”的总和。
每个字母都有一个“漂亮度”，范围在1到26之间。没有任何两个字母拥有相同的“漂亮度”。字母忽略大小写。
给出多个名字，计算每个名字最大可能的“漂亮度”。

from collections import Counter

while True:
    try:
        a = int(input())
        for i in range(a):
            c, start, res = Counter(input()), 26, 0
            for j in c.most_common():
                res += j[1] * start
                start -= 1
            print(res)

    except:
        break
注：most_comman返回一个TopN列表。如果n没有被指定，则返回所有元素。当多个元素计数值相同时，排列是无确定顺序的

70. 查找和排序


def rank_record(inp_num, rank_rule):
    dic_name = []
    while (inp_num > 0):
        inp_name = input()
        dic_name.append(inp_name)
        inp_num -= 1
    inp_name_sort = sorted(dic_name, key=lambda a: int(a.split(' ')[1]), reverse=(rank_rule - 1))
    return inp_name_sort


while True:
    try:
        inp_num = int(input())
        rank_rule = int(input())
        for i in rank_record(inp_num, rank_rule):
            print(i)
    except:
        break
