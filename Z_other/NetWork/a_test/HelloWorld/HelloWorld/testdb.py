# -*- coding: utf-8  -*-
# -*- author: jokker -*-

from django.http import HttpResponse

# from ..TestModel.models import Test


# def testdb(request):
#     # test1 = Test(name='runoob')
#     # test1.save()
#     return HttpResponse("<p>数据添加成功！</p>")

def testdb(request):
    return HttpResponse("Hello world")