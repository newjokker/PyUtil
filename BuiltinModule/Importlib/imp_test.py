# -*- coding: utf-8  -*-
# -*- author: jokker -*-

"""
模块的重载试验

* 【注意】输入的参数必须要是模块名，而不是类名或者是函数名

"""


import importlib

import BuiltinModule.Importlib.test_function as test


test.Test.show()

importlib.reload(test)


test.Test.show()