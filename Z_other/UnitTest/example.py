# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import unittest

# 1. setUp()、tearDown()，分别在每调用一个测试方法的前后分别被执行

# 2. 期待跑出指定的错误， with self.assertRaises(KeyError): value = d['empty']，比如通过d['empty']访问不存在的key时，断言会抛出KeyError

# 3. 断言是否相等，self.assertEquals(d.a, 1),  # 断言函数返回的结果与1相等

from Z_other.JoUtil.JoList import JoList


class TestDict(unittest.TestCase):

    def setUp(self):
        """程序运行的时候执行"""
        print('before test')

    def test_add(self):
        """测试 add 魔法方法"""
        a, b, c = JoList([1, 2, 3, 4, 5]), JoList([6, 7, 8, 9, 10]), JoList()
        self.assertEquals(a + b, JoList([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))

    def test_sub(self):
        """测试 sub 方法"""
        a, b, c = JoList([1, 2, 3, 4, 5]), JoList([6, 7, 8, 9, 10]), JoList()
        self.assertEquals(a - b, JoList([1, 2, 3, 4, 5]))

    def test_choose(self):
        """测试 choose 函数"""
        a = JoList([1, 2, 3, 4, 5])
        b = JoList([1, 5, 8])
        self.assertEquals(a.choose(b), JoList([1, 5]))

    def tearDown(self):
        """在方法最后执行"""
        print('after test')


if __name__ == '__main__':
    unittest.main()
