# -*- coding: utf-8  -*-
# -*- author: jokker -*-

# 参考 ： https://www.cnblogs.com/golinux/p/10809979.html

"""
* r (read)	只读模式,不能写（文件必须存在，不存在会报错）
* w (write)	只写模式,不能读（文件存在则会被覆盖内容（要千万注意），文件不存在则创建）
* a (append)	追加模式,不能读
* r+	读写模式
* w+	写读模式
* a+	追加读模式
* rb	二进制读模式
* wb	二进制写模式
* ab	二进制追加模式
* rb+	二进制读写模式
* wb+	二进制写读模式
* ab+	二进制追加读模式
"""

# f = open(r'C:\Users\Administrator\Desktop\for6.png', encoding="utf-8")

# f.open()

# f.close()

# tell()　　获取当前的读取数据的位置(可以理解为一个读光标当前的位置)

# seek(n)　　从第n个字符开始读取(将读光标移动到第n个字符)

# read : 是读整个文件在光标后面的所有字符(包括光标所在的那个字符)，读完后，会把光标移到你读完的位置

# readline : 读光标所在这一行的在光标后面的所有字符(包括光标所在的那个字符)，读完后，会把光标移到你读完的位置

# readlines : 和read类似，但把读的字符按行来区分做成了列表

# 对于 list、tuple、dict、set 的数据需要使用二进制的方式读写，否则写入或读出的数据可能会乱码

# 编码用的什么字符集，解码也需要用同样的字符集

# 要注意文件本身自带的编解码和写入读出的手动编解码是两回事
# with open("1.txt",mode="wb") as f1:
#     str1 = "xianqian嘿嘿"
#     f1.write(str1.encode("utf-8"))


# with open("1.txt", mode="rb") as f2:
#     data = f2.read()
#     # data = f2.read().decode("utf-8")
