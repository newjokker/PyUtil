# -*- coding: utf-8  -*-
# -*- author: jokker -*-



class Exam(object):

    """
    老师想知道从某某同学当中，分数最高的是多少，现在请你编程模拟老师的询问。当然，老师有时候需要更新某位同学的成绩.

    输入描述:
    输入包括多组测试数据。
    每组输入第一行是两个正整数N和M（0 < N <= 30000,0 < M < 5000）,分别代表学生的数目和操作的数目。
    学生ID编号从1编到N。
    第二行包含N个整数，代表这N个学生的初始成绩，其中第i个数代表ID为i的学生的成绩
    接下来又M行，每一行有一个字符C（只取‘Q’或‘U’），和两个正整数A,B,当C为'Q'的时候, 表示这是一条询问操作，他询问ID从A到B（包括A,B）的学生当中，成绩最高的是多少
    当C为‘U’的时候，表示这是一条更新操作，要求把ID为A的学生的成绩更改为B。
    """
    @staticmethod
    def test_001():

        try:
            while True:
                N_str, M_str = input().strip().split(' ')
                N, M = int(N_str), int(M_str)
                stu_grades = list(map(lambda x: int(x), input().strip().split(' ')))
                for i in range(M):
                    C, A_str, B_str = input().strip().split(' ')
                    A, B = int(A_str), int(B_str)
                    if C == 'Q':
                        if A > B:
                            A, B = B, A
                        print(max(stu_grades[A - 1:B]))
                    elif C == 'U':
                        stu_grades[A - 1] = B
        except:
            pass

    """
    开发一个简单错误记录功能小模块，能够记录出错的代码所在的文件名称和行号。 
    处理:
    1.记录最多8条错误记录，对相同的错误记录(即文件名称和行号完全匹配)只记录一条，错误计数增加；(文件所在的目录不同，文件名和行号相同也要合并)
    2.超过16个字符的文件名称，只记录文件的最后有效16个字符；(如果文件名不同，而只是文件名的后16个字符和行号相同，也不要合并)
    3.输入的文件可能带路径，记录文件名称不能带路径
    
    # 输入
    一行或多行字符串。每行包括带路径文件名称，行号，以空格隔开。
    文件路径为windows格式
    如：E:\V1R2\product\fpgadrive.c 1325
    
    # 输出
    将所有的记录统计并将结果输出，格式：文件名代码行数数目，一个空格隔开，如: fpgadrive.c 1325 1 
    结果根据数目从多到少排序，数目相同的情况下，按照输入第一次出现顺序排序。
    如果超过8条记录，则只输出前8条记录.
    如果文件名的长度超过16个字符，则只输出后16个字符
    """
    @staticmethod
    def test_002():
        import collections
        or_dict = collections.OrderedDict()
        try:
            while True:
                x = input()
                i = x.rfind('\\')
                q = x[i + 1:]
                if q in or_dict:
                    or_dict[q] += 1
                else:
                    or_dict[q] = 1
        except:
            or_dict = sorted(or_dict.items(), key=lambda k: k[1], reverse=True)
            for i in range(min(len(or_dict), 8)):
                t = or_dict[i][0].split(' ')
                print(t[0][-16:], t[1], or_dict[i][1])

    """
    扑克牌游戏大家应该都比较熟悉了，一副牌由54张组成，含3~A，2各4张，小王1张，大王1张。牌面从小到大用如下字符和字符串表示（其中，小写joker表示小王，大写JOKER表示大王）:) 
    3 4 5 6 7 8 9 10 J Q K A 2 joker JOKER 
    输入两手牌，两手牌之间用“-”连接，每手牌的每张牌以空格分隔，“-”两边没有空格，如：4 4 4 4-joker JOKER
    请比较两手牌大小，输出较大的牌，如果不存在比较关系则输出ERROR
    
    基本规则：
    （1）输入每手牌可能是个子，对子，顺子（连续5张），三个，炸弹（四个）和对王中的一种，不存在其他情况，由输入保证两手牌都是合法的，顺子已经从小到大排列；
    （2）除了炸弹和对王可以和所有牌比较之外，其他类型的牌只能跟相同类型的存在比较关系（如，对子跟对子比较，三个跟三个比较），不考虑拆牌情况（如：将对子拆分成个子）
    （3）大小规则跟大家平时了解的常见规则相同，个子，对子，三个比较牌面大小；顺子比较最小牌大小；炸弹大于前面所有的牌，炸弹之间比较牌面大小；对王是最大的牌；
    （4）输入的两手牌不会出现相等的情况。
    答案提示：
    （1）除了炸弹和对王之外，其他必须同类型比较。
    （2）输入已经保证合法性，不用检查输入是否是合法的牌。
    （3）输入的顺子已经经过从小到大排序，因此不用再排序了.
    """
    @staticmethod
    def test_003():

        A = '3 4 5 6 7 8 9 10 J Q K A 2 joker JOKER'.split(' ')

        try:
            while True:
                s = input().strip()
                a, b = s.split('-')
                w = None
                p, q = a.split(' '), b.split(' ')
                if len(q) != len(p):
                    for t in p, q:
                        if len(t) == 2 and t[0] == 'joker':
                            w = ' '.join(t)
                            break
                        elif len(t) == 4:
                            w = ' '.join(t)
                    if not w:
                        w = 'ERROR'
                elif A.index(q[0]) > A.index(p[0]):
                    w = b
                else:
                    w = a
                print(w)
        except:
            pass

