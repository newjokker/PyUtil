# -*- coding: utf-8  -*-
# -*- author: jokker -*-

with open(r'C:\Users\Administrator\Desktop\duanzi.txt') as txt_file:
    for each_line in txt_file:

        each_line = each_line.lstrip('"')
        # each_line = each_line.rstrip('"')

        print(each_line)




