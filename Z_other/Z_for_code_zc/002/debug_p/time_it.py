# -*- coding: utf-8  -*-
# -*- author: jokker -*-


from Decorator.time_it import timethis
import time


@timethis
def main():
    time.sleep(2)

@timethis
def test_001():
    for i in range(100000):
        a = []
        a.append(i)
        del a


if __name__ == "__main__":

    main()

    test_001()