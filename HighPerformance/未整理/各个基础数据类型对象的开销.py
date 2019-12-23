# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import sys

print('str : ', sys.getsizeof(''))
print('int : ', sys.getsizeof(int()))
print('float : ', sys.getsizeof(float()))
print('list : ', sys.getsizeof(list()))
print('dict : ', sys.getsizeof(dict()))
print('set : ', sys.getsizeof(set()))
print('tuple : ', sys.getsizeof(tuple()))