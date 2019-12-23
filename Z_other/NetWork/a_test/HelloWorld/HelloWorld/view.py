# -*- coding: utf-8  -*-
# -*- author: jokker -*-

from django.http import HttpResponse
from django.shortcuts import render


# def hello(request):
#     return HttpResponse("Hello world")


def jokker(request):
    context = {'hello': 'Hello World!',
               'name': 'Jokker'}
    return render(request, 'jokker/jokker.html', context)  # 第二个参数是相对目录


def hello(request):
    return render(request, 'cainiao.html')


def cainiao(request):
    return render(request, 'cainiao.html')










