# -*- coding: utf-8  -*-
# -*- author: jokker -*-


def test(n):

    if n == 0:
        return 0
    elif n == 1:
        return 1

    index = 2
    i, j = 0, 1
    while index <= n:
        index += 1
        i, j = j, i+j
    return j



if __name__ == "__main__":

    print(test(7))




