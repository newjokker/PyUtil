# -*- coding: utf-8  -*-
# -*- author: jokker -*-

sql_str = """create table student3(name varchar(30) comment '姓名',
age smallint comment '年龄',sex enum('男','女') comment '性别',primary key(name,age)
)engine = myisam,charset = utf8,comment = '学生表'"""

from Report.MySqlUtil import MySqlUtil


a = MySqlUtil()
host, port, user, passwd, db_name = 'localhost', 3306, 'root','747225581', "jokker"
a.conoect_mysql(host, port, user, passwd, db_name)
a.execute(sql_str)


