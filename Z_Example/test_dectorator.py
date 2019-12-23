# -*- coding: utf-8  -*-
# -*- author: jokker -*-


from Decorator.goodLuck import TextWaterfall



@TextWaterfall.no_bug_forever
def ok():
    print('ok')


if __name__ == '__main__':


    ok()