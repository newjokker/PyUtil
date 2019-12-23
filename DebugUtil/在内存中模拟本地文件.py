# -*- coding: utf-8  -*-
# -*- author: jokker -*-

# 参考： https://blog.csdn.net/zengxiantao1994/article/details/60466087, https://www.jianshu.com/p/77834701be2a


"""

"""


from io import StringIO


s = StringIO()
s.write("www.baidu.com\n")
s.write("news.realsil.com.cn")
# getvalue() 方法用于获取写入后的str
print(s.getvalue())

# 也可以像读取文件一样读取StringIO中的数据
s.seek(0)
while True:
    strBuf = s.readline()
    if strBuf == "":
        break

    print(strBuf.strip())

s.close()

