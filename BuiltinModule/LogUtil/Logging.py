# -*- coding: utf-8  -*-
# -*- author: jokker -*-

# 一个日志记录的装饰器

from functools import wraps
import logging


def logged(level, name=None, message=None):
    """
    可以传参的日志记录
    :param level:
    :param name:
    :param message:
    :return:
    """

    def decorate(func):
        logname = name if name else func.__module__
        log = logging.getLogger(logname)
        logmsg = message if message else func.__name__

        @wraps(func)
        def wrapper(*args, **kwargs):
            log.log(level, logmsg)
            return func(*args, **kwargs)

        return wrapper

    return decorate


@logged(3, 'ok', '记录 OK的信息')
def ok():
    print('ok')


if __name__ == '__main__':
    ok()
