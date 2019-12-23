#!D:\Anaconda\envs\python36_all
# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import random
import time
import sys


def main():
    txt_path = r'E:\Algorithm\Util_Util\Z_for_CSDN\the_art_of_war\AuxData\the art of war.txt'

    with open(txt_path, 'r', encoding='utf-8') as txt_file:
        txt_list = ''.join(txt_file.readlines()).split('。')

    while True:
        input()
        print(random.choice(txt_list))


if __name__ == "__main__":

    main()
