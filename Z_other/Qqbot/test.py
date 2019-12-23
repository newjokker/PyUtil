

# FIXME 单例模式实验

class jokker(object):

    def __init__(self, name):
        self.__name = name

    def get_instance(self):
        return jokker



class Foo(object):

    instance = None

    def __init__(self, name):
        self.name = name

    @classmethod
    def get_instance(cls):
        if cls.instance:
            return cls.instance
        else:
            obj = cls('hexm')
            cls.instance = obj
            return obj



a  = Foo.get_instance()
print(a)
b  = Foo.get_instance()
print(b)


c  = jokker(12)
print(c)
d  = jokker(34)
print(d)
