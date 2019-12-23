# -*- coding: utf-8  -*-
# -*- author: jokker -*-


def ok():
    list_i = []
    while True:
        if len(list_i) == 0:
            list_i = [1]
            yield list_i
        if len(list_i) == 1:
            list_i = [1, 1]
            yield [1, 1]
        else:
            res = [1]
            for i in range(len(list_i)-1):
                res.append(list_i[i] + list_i[i+1])
            res.append(1)
            list_i = res.copy()
            yield list_i

ii = 0
for i in ok():
    ii += 1
    if ii > 20:
        break
    print(i)
