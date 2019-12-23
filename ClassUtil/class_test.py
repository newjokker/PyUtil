# -*- coding: utf-8  -*-
# -*- author: jokker -*-




class Test(object):

    def __repr__(self):
        """返回实例的代码表示"""
        return 'ok'

    def __str__(self):
        """定义调用 str 的时候返回值"""
        return 'Test'

    def __format__(self, format_spec=''):
        """自定义字符串的输出格式"""
        if format_spec == '':
            format_spec = 'ymd'
        return format_spec

    # ----------------- 支持上下文管理协议 -----------------
    """
    上下文管理器的作用
    
    
    """


    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass





if __name__ == "__main__":

    a = Test()

    print(a)
    print(format(a, 'a'))
