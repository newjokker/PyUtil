# -*- coding: utf-8  -*-
# -*- author: jokker -*-


from Report.FTPUtil import FTPUtil

# Host = 'rsapp.nsmc.org.cn'
Ip = '211.154.196.5'
userName = 'proftp001'
passWord = 'j171dWVx'
a = FTPUtil()
a.login(userName, passWord, port=2221, ip=Ip)
a.clone_dir(r'/SCLS/H8Fire/20190918/201909181440', r'C:\Users\Administrator\Desktop\hehe', print_detail=True)

