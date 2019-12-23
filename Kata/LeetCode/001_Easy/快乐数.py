# -*- coding: utf-8  -*-
# -*- author: jokker -*-

def test(n):

    res = n
    not_happy = set()

    while True:
        res = list(str(res))
        res = str(sum(list(map(lambda x: int(x)**2, res))))
        print(res)
        if res == '1':
            return True
        elif res in not_happy:
            return False
        not_happy.add(res)



if __name__ == "__main__":

    print(test(19234567))


