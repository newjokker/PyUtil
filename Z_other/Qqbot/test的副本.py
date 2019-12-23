# -*- coding: utf-8 -*-
import re

dataDict = {"qq":"747225581",
    "weixin":"18761609908"}


# 一个回复对象
class message:
    """一条记录对象"""

    def __init__(self, typeTemp=None, contentTemp=[], infoTemp=None):
        self.__type     = typeTemp
        self.__content  = contentTemp
        self.__info     = infoTemp

    def set_info(self, infoTemp):
        """设置备注信息"""
        if isinstance(infoTemp, str):
            self.__info = infoTemp

    def set_type(self, typeTemp):
        if typeTemp in ["@", "?", "answer"]:
            self.__type = typeTemp

    def set_content(self, contentTemp):
        """设置content列表"""
        # 当传入的是不为空的列表
        if isinstance(contentTemp, list) and contentTemp:
            self.__content = contentTemp

    def print_message(self):
        """打印当前信息"""
        print("type     : {0}".format(str(self.__type)))
        print("content  : {0}".format(str(self.__content)))
        print("info     : {0}".format(str(self.__info)))

    def get_type(self):
        return self.__type

    def get_content(self):
        return self.__content

    def get_info(self):
        return self.__info

class task:

    def __init__(self, taskState=False, taskName="", taskInfo=""):
        self.__state    = taskState
        self.__name     = taskName
        self.__info     = taskInfo

    def task_describe(self):
        print("task: {0}, status: {1}, info: {2}".format(self.__name, self.__state, self.__info))

def get_message(resStr):
    """获得 message 对象"""
    # 对输入字符串去除两端空格
    resStr = resStr.strip(" ")
    # 初始化 message 类
    resMessage = message()

    # 信息头
    head = resStr[0]

    # 第一个级别，
    if head == "@":
        resMessage.set_type("@")
    elif head == "?":
        resMessage.set_type("?")
    else:
        resMessage.set_type("answer")

    # 如果不是 answer 去掉第一个功能字符
    if resMessage.get_type() != "answer":
        nowRes = resStr[1:]
    else:
        nowRes = resStr

    # 第二个级别
    if ":" in nowRes:
        index = nowRes.find(":")
        resMessage.set_info(nowRes[index+1:])
        content = nowRes[:index]
    else:
        content = nowRes

    # 第三个级别 content 分割
    tempContent = []
    for eachElement in re.split(r'[, ]', content):
        if eachElement.strip(" "):
            tempContent.append(eachElement)
    resMessage.set_content(tempContent)

    return resMessage

def analysis_record(messageTemp):
    """解析记录形输入"""
    # 判断输入类型是否为 message
    if not isinstance(messageTemp, message):
        return

    # 当 content 为空, 或者关键字不在需要的字典中
    if not messageTemp.get_content():
        return

    # 当要记录的元素不在字典中的时候
    taskName = messageTemp.get_content()[0]
    if taskName not in ["吃蛋", "吃饭", "刷牙", "记录", "反省"]:
        return

    # 当前完成状态
    state = False
    if len(messageTemp.get_content()) <= 1:
        state = True
    elif str(messageTemp.get_content()[1]).lower() in ["true", "1", "ok", "bingo", "完成", "实现"]:
        state = True

    return task(taskState=state, taskInfo=messageTemp.get_info(), taskName=taskName)

def analysis_question():
    """解析询问形输入"""
    pass

def analysis_anaswer():
    """解析回答形输入"""
    pass

def analysis_message():
    """解析 message 所包含的信息"""
    pass


while True:

    res = input(":")
    res = res.strip(" ")
    # 为 q 退出
    if res == "q":
        break
    # 为 "" 继续
    elif not res:
        continue

    # -- -- -- -- -- -- -- -- -- -- -- -- -- -- 获取 message 信息

    a = get_message(res)

    a.print_message()

    if a.get_type() == "@":
        b = analysis_record(a)
        if b:
            b.task_describe()


    # # -- -- -- -- -- -- -- -- -- -- -- -- -- -- 解析 message
    # # 每一个事项用一个类来表示，这样更加清楚容易
    # nowAnswer = "当前事项"
    # answerDict = {}
    #
    # typeTemp    = message["type"]
    # contentTemp = message["content"]
    # infoTemp    = message["info"]
    #
    #
    #
    # if typeTemp == "answer":
    #     """回答上一条信息"""
    #     messageAnswer = nowAnswer
    #     pass
    # elif typeTemp == "@":
    #     messageAnswer = content[0]







