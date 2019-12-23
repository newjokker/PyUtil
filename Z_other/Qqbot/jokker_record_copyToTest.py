# -*- coding: utf-8 -*-
import re
import os

# FIXME 需要新增的功能，修改功能字典，那些字典都可以自己增改

# FIXME 保存到本地文件

# FIXME 可以将写的函数放到系统默认的文件夹，这样就能直接 import 了，应该就不会报错了

"""
Qqbot -q 1027846080
qq plug Qqbot.plugins.test
"""

class task(object):
    """一个任务"""

    def __init__(self):
        self.__state = False
        self.__name = []
        self.__info = ""
        self.__cycle = None

    def task_describe(self):
        """描述任务"""
        return "task: {0}, status: {1}, info: {2}".format(",".join(self.__name), self.__state, self.__info)

    def set_status(self, status):
        """设置任务是否完成"""
        if status:
            self.__state = True

    def set_name(self, tempName):
        """设置任务的名字，因为任务可能有多个名字，所以用列表的方式进行存储"""
        if isinstance(tempName, list):
            self.__name = tempName

    def set_info(self, tempInfo):
        """任务描述，用于接受 ：后面的语句"""
        if isinstance(tempInfo, str):
            self.__info = tempInfo

    def set_cycle(self, tempCycle):
        """设置周期，以小时为单位"""
        if isinstance(tempCycle, int):
            self.__cycle = tempCycle

class answer(object):
    """一条询问的回答"""

class message(object):
    """一条记录对象"""

    def __init__(self, typeTemp=None, contentTemp=[], infoTemp=None):
        self.__type = typeTemp
        self.__content = contentTemp
        self.__info = infoTemp

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

class needFunction(object):

    @staticmethod
    def read_setting(seetingFilePath):
        """读取第一种设置文件的方法，只以逗号相间隔，去掉空格和tab"""
        result = []
        with open(seetingFilePath, 'r') as txtFile:
            for eachLine in  txtFile:
                # 数据以 , ， \t 和 space
                for eachElement in re.split(r'[, ，\t\n]', eachLine):
                    if eachElement:
                        result.append(eachElement)
        return result

    @staticmethod
    def read_task_file(seetingFilePath):
        """第二种读取设置文件的方式，专门读取 task 文件设置"""
        result = []
        with open(seetingFilePath, 'r') as txtFile:
            txtData = txtFile.readlines()

        # 初始化的任务只有 名字 和 周期信息
        for eachLine in  txtData:
            # 去掉只有换行和空格的行
            if not eachLine.strip("\n").strip(" "):
                continue

            # 只能不是有一个 ":" 用于分割
            taskData = re.split('[:：]', eachLine)
            if len(taskData) != 2:
                continue

            taskNameTemp = []
            # 当名字多余等于一个
            for eachName in re.split('[, ，    ]', taskData[0]):
                eachNameTemp = eachName.strip(' ').strip('  ')
                if eachNameTemp:
                    taskNameTemp.append(eachNameTemp)
            # 当周期为整数的时候
            taskCycleTemp = taskData[1].strip('\n').strip(" ")
            if not taskCycleTemp.isnumeric():
                taskCycleTemp = None

            if taskCycleTemp and taskNameTemp:
                tempTask = task()
                tempTask.set_cycle(int(taskCycleTemp))
                tempTask.set_name(taskNameTemp)
                result.append(tempTask)

        return result

    @staticmethod
    def read_data_dict(dataDictFolder):
        """第三种读取文件的方法，用于读取本地查询字典，读取整个文件夹"""

        def openTxt(txtPath):
            """打开一个txt文件"""
            resultTemp = {}
            with open(txtPath, 'r') as txtFile:
                txtData = txtFile.readlines()

            # 初始化的任务只有 名字 和 周期信息
            for eachLine in txtData:
                # 去掉只有换行和空格的行
                if not eachLine.strip("\n").strip(" "):
                    continue

                # 只能不是有一个 ":" 用于分割
                dataLineTemp = re.split('[:：]', eachLine)
                if len(dataLineTemp) != 2:
                    continue

                keyStr, valueStr = [], []

                for eachKey in re.split('[ ,，    ]', dataLineTemp[0]):
                    nowKey = eachKey.strip(" ").strip('\n')
                    if nowKey:
                        keyStr.append(nowKey)

                for eachValue in re.split('[ ,，    ]', dataLineTemp[1]):
                    nowValue = eachValue.strip(" ").strip('\n')
                    if nowValue:
                        valueStr.append(eachValue.strip())

                if keyStr and valueStr:
                    for eachKeyTemp in keyStr:
                        resultTemp[eachKeyTemp] = valueStr

            return resultTemp

        result = {}
        for eachFile in os.listdir(dataDictFolder):
            # 是 .txt 文件
            if eachFile.endswith(".txt"):
                abstructPath = os.path.join(dataDictFolder, eachFile)
                txtDictTemp = openTxt(abstructPath)
                if txtDictTemp:
                    result.update(txtDictTemp)

        return result

class constant(object):
    """设置参数"""

    # 任务
    tasks = needFunction.read_task_file(r'./settingFile/task.txt')

    # 表示完成的字符串
    beTrue = needFunction.read_setting(r'./settingFile/beTrue.txt')
    # 表示未完成的字符串
    beFalse = needFunction.read_setting(r'./settingFile/beFalse.txt')
    # 记录符号
    recordType = needFunction.read_setting(r'./settingFile/recordType.txt')
    # 询问符号
    questionType = needFunction.read_setting(r'./settingFile/questionType.txt')

    # 查询字典
    dataDict = needFunction.read_data_dict(r'./dataDict')

class task_robort(object):
    """任务机器人"""

    instance = None

    # FIXME 需不需要给每一个任务简历一个文件，然后这样可以往里面增加更多的信息了，或者使用一个 xml 文件进行读写

    def __init__(self):

        # 当前任务
        self.__task_now = None
        # 待做任务列表
        self.__task_todo = []
        # 已完成任务列表
        self.__task_done = []

    def next_task(self):
        """当前任务完成了，放到task_done 否则 放入 task_todo ; 切换当前任务"""
        pass

    def find_suited_task(self):
        """找到适合的任务，任务都有时间范围限定，找到合适的任务，并返回其中一个"""
        pass

    def save_to_file(self):
        """将任务完成信息写入到本地"""
        # 当前时间，已完成任务，未完成任务，
        pass

    @staticmethod
    def get_instance(cls):
        """新建一个 task_robort 单例"""
        if cls.instance:
            return cls.instance
        else:
            obj = cls()
            cls.instance = obj
            return obj

class dataDict(object):
    """查询的信息字典，这个要用单例模式"""

    def __init__(self, questionStr, pickNum, whereStr):
        self.__question = questionStr

        self.__pickNum = "*"
        if not pickNum == '*':
            self.__pickNum = int(pickNum)

        self.__where = whereStr
        self.__answer = None

    def find_answer(self):
        """在数据库中找到需要的内容"""

        keyWord = self.__question[0]

        # 当需要查找的是 log 信息的时候
        if keyWord in ['log', '历史']:
            """返回 今天的 log 数据"""
            pass

        # 当需要查找的是 设置信息的时候
        if keyWord in ['seeting', 'set']:
            """返回对应的设置信息"""
            pass

        # 去常量字典中找需要的信息
        if keyWord in constant.dataDict:
            if self.__pickNum == "*":
                self.__answer = constant.dataDict[keyWord]
            else:
                self.__answer = constant.dataDict[keyWord][:self.__pickNum]

    def describe_question(self):
        """描述问题"""

        self.find_answer()

        if self.__answer:
            return self.__answer

        describeStr = "your question is : {0}, your pick {1} piece of answer , and you use {2} to limit your question".format(
            str(self.__question), self.__pickNum, self.__where)

        return describeStr

class analysisMessage:
    """分析message包含的信息"""

    def __init__(self, response):
        self.__res = response
        self.__message = message()
        self.__response = None

    def get_message(self):
        """获得 message 对象"""
        # 对输入字符串去除两端空格
        resStr = self.__res
        resStr = resStr.strip(" ")
        # 初始化 message 类
        resMessage = message()

        # 当输入为空的时候，继续
        if not resStr:
            return

        # 信息头
        head = resStr[0]

        # 第一个级别，
        if head in constant.recordType:
            resMessage.set_type("@")
        elif head in constant.questionType:
            resMessage.set_type("?")
        else:
            resMessage.set_type("answer")

        # 如果不是 answer 去掉第一个功能字符
        if resMessage.get_type() != "answer":
            nowRes = resStr[1:]
        else:
            nowRes = resStr

        # 第二个级别
        if ":" in nowRes or "：" in nowRes:
            index = nowRes.find(":")
            if index == -1:
                index = nowRes.find("：")
            resMessage.set_info(nowRes[index + 1:])
            content = nowRes[:index]
        else:
            content = nowRes

        # 第三个级别 content 分割
        tempContent = []
        for eachElement in re.split(r'[, ，]', content):
            if eachElement.strip(" "):
                tempContent.append(eachElement)
        resMessage.set_content(tempContent)

        self.__message = resMessage

        resMessage.print_message()

    def analysis_message(self):
        messageType = self.__message.get_type()
        if messageType == "@":
            self.__analysis_record()

        elif messageType == "?":
            if self.__analysis_question():
                return True
        elif messageType == "answer":
            if self.__analysis_answer():
                return True

    def describe_message(self):
        """描述message"""
        describeMessage = """ type    : {0} \n comment : {1} \n  info    : {2}""".format(self.__message.get_type(),
                                                                                         str(
                                                                                             self.__message.get_content()),
                                                                                         self.__message.get_info())

        return describeMessage

    def get_response(self):
        return self.__response

    def do_process(self):
        self.get_message()
        self.analysis_message()

    def __analysis_record(self):
        """解析记录形输入"""
        # 判断输入类型是否为 message
        messageTemp = self.__message
        if not isinstance(messageTemp, message):
            print("输入数据不是message结构")
            return

        # 当 content 为空, 或者关键字不在需要的字典中
        if not messageTemp.get_content():
            print("content为空")
            return

        # FIXME 写核对任务列表的代码
        # # 当要记录的元素不在字典中的时候
        taskName = messageTemp.get_content()[0]
        # if taskName not in constant.tasks:
        #     return

        # 当前完成状态
        state = False
        if len(messageTemp.get_content()) <= 1:
            state = True
        elif str(messageTemp.get_content()[1]).lower() in constant.beTrue:
            state = True
        elif str(messageTemp.get_content()[1]).lower() in constant.beFalse:
            state = False

        taskTemp = task()
        taskTemp.set_name([taskName])
        taskTemp.set_status(state)
        taskTemp.set_info(messageTemp.get_info())

        self.__response = taskTemp.task_describe()

    def __analysis_question(self):
        """解析询问形输入"""
        # 询问的回复
        contentTemp, infoTemp = self.__message.get_content(), self.__message.get_info()

        if not isinstance(contentTemp, list):
            return

        pickNum, questionStr = "*", contentTemp
        if len(contentTemp) >= 1:
            # 如果第一个关键词是需要的限制返回值多少的字符
            if contentTemp[0] in ["*"] or contentTemp[0].isnumeric():
                # 第一个是数量限定词，第二个是关键字，所以需要最少两个元素
                if len(contentTemp) >= 2:
                    # 返回元素个数
                    pickNum = contentTemp[0]
                    # 问题语句
                    questionStr = contentTemp[1:]
            else:
                if len(contentTemp)>=1:
                    pickNum = "*"
                    questionStr = contentTemp

        a = dataDict(questionStr, pickNum, infoTemp)
        self.__response = a.describe_question()

        # FIXME 在信息字典中找到问题的答案，传入 questionStr（strList），这里的 info 可以作为 where 关键词来使用的，
        # 根据问题字段，返回答案
        # answerTemp = None
        # if questionStr[0] in constant.constant:
        #     answerTemp = constant.constant[questionStr[0]]


        # # 如果没有回答，直接退出程序
        # if not answerTemp:
        #     return
        #
        # # 根据 pickNum 返回对应的数据条数
        # if pickNum == "*":
        #     self.__response = answerTemp
        # else:
        #     self.__response = answerTemp[:int(pickNum)]

    def __analysis_answer(self):
        """解析回答形输入"""
        # return "识别为 answer 模式，需要进一步分析"
        return False

while True:

    # aa = constant.tasks
    # bb = constant.dataDict
    # break

    res = input("输入命令")
    res = str(res)

    if res == "q":
        break

    print('-'*150)
    a = analysisMessage(res)
    a.do_process()

    print('-'*150)
    print(a.get_response())
    print('-'*150)













