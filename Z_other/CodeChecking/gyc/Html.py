# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

class Html():
    '''HTML模板替换'''

    def __init__(self,inputHtmlDir,outputHtmlDir):
        ''' 初始化    输入路径 / 输出路径'''
        self.inputHtmlDir = inputHtmlDir
        self.outputHtmlDir = outputHtmlDir

        self.soup = ''

    def getsoup(self):
        return BeautifulSoup(open(self.inputHtmlDir), features="lxml")

    def writesoup(self,soup):
        with file(self.outputHtmlDir, "w") as htmlFile:
            htmlFile.write(str(soup))

class textRplace(Html):
    ''' 文本替换'''
    def __init__(self,inputHtmlDir,outputHtmlDir,keywords):
        Html.__init__(self,inputHtmlDir,outputHtmlDir)
        self.keywords = keywords  #替换文本字典

        self.textlabel = 'div'  #替换标签     # FIXME 替换标签需要变为可变参数

    def writeReport(self):
        '''文本替换流程'''
        soup = self.replaceText(self.getsoup())
        self.writesoup(soup)

    def replaceText(self,soup):
        for key in self.keywords.keys():
            value = self.keywords[key]
            ComStr = soup.findAll(self.textlabel,text=key)  # 找到所有替换标签对应的文本符合要求的部分
            for item in range(len(ComStr)):
                ComStr[item].string = str(value)
        return  soup

class pictureFill(Html):
    '''图片替换'''

    def __init__(self,inputHtmlDir,outputHtmlDir,pictureDir,PluginName):
        Html.__init__(self,inputHtmlDir,outputHtmlDir)
        self.picture = pictureDir  # FIXME  变量名使用不合适，明明就是个 list 很容易联想到时一个 pic 对象或者 picpath
        self.PluginName = PluginName

        self.IPPath = "http://10.129.55.149:8080/FileServer/"
        self.PicPathList = []
        self.label = "img"

    def writeReport(self):
        '''图片替换流程'''
        self.preparePic()
        soup = self.getsoup()
        pic = soup.find_all(self.label)
        for item in range(len(pic)):
            pic[item]['src'] = self.PicPathList[item]
        self.writesoup(soup)

    def preparePic(self):
        '''图片准备'''
        if isinstance(self.picture,list):
            for item in self.picture:
                self.PicPathList.append(self.getPicPathInfo(item))
        else:
            self.PicPathList.append(self.getPicPathInfo(self.picture))

    def getPicPathInfo(self,ConstMapInfo):
        '''图片路径转http   Input:图片绝对路径'''
        path = ConstMapInfo.replace("\\", "/")
        splitPath = path.split("/")
        index = splitPath.index(self.PluginName)
        RelativePath = splitPath[index:]
        pathname = self.IPPath + "/".join(RelativePath)
        return pathname

class tableRplace(Html):
    '''表格替换'''
    def __init__(self,inputHtmlDir,outputHtmlDir,inputlist,replace_key):
        Html.__init__(self, inputHtmlDir, outputHtmlDir)
        self.inputlist = inputlist  # 输入表格
        self.replace_key = replace_key

    def getTable(self):
        '''表格替换流程'''
        outputtag = self.preparelist()
        with open(self.outputHtmlDir, 'r') as Fobj:
            temp_html = ''.join(Fobj.readlines())
        with open(self.outputHtmlDir, 'w') as Fobj:
            Fobj.writelines(temp_html.replace(self.replace_key,outputtag))

    def preparelist(self):
        '''表格准备'''
        outputtag = ''
        if isinstance(self.inputlist,list):
            for item in range(len(self.inputlist)):
                outputtag += self.listToline(self.inputlist[item])
        else:
            outputtag +=self.listToline(self.inputlist)
        return outputtag

    def listToline(self,inputlist):
        '''返回HTML格式的表形式  分为表头以及表身    Input:list'''
        tr = ''
        tr += '<tr>'
        for item in inputlist:
            tr += self.tdlable(item,width = '92')
        tr += '</tr>'
        return  tr

    def tdlable(self,item,height='30',width='100',fontsize='10.5',font_family='Times New Roman',color='#00000a',rtical_align='middle'):
        td = ''
        td += '<td style="height:'+height+'px;rtical-align:'+rtical_align+'; width:'+width+'px">'
        td += '<p style="td-align:center">'
        td += '<span style="font-size:'+fontsize+'pt;font-family:\''+font_family+'\';color:'+color+'">'
        td += str(item)
        td += '</span>'
        td += '</p>'
        td += '</td>'
        return td



class HtmlWrite(object):

    def __init__(self, html):
        self.soup = BeautifulSoup(open(html), features="lxml")  # 解析 html

    def txt_replace_in_assign_tag(self, assign_tag, keywords):
        """替换指定标签下的文本"""

        for key in keywords:
            ComStr = self.soup.findAll(assign_tag, text=key)  # 找到所有替换标签对应的文本符合要求的部分
            for each in ComStr:
                each.string = keywords[key]
                print(u'{0} ==> {1}'.format(key, keywords[key]))

    def pic_fill(self, pic_list, PluginName, IPPath, assign_tag):
        """图片替换"""
        PicPathList = []
        if isinstance(pic_list, list):
            for item in pic_list:
                PicPathList.append(self.getPicPathInfo(item, PluginName, IPPath))  # FIXME 就是将图片的地址拼为需要的地址，这么写是有问题的
        else:
            PicPathList.append(self.getPicPathInfo(pic_list, PluginName, IPPath))

        pic = self.soup.find_all(assign_tag)

        for item in range(len(pic)):
            pic[item]['src'] = PicPathList[item]

    @staticmethod
    def getPicPathInfo(ConstMapInfo, PluginName, IPPath):
        """对图片路径进行清洗操作"""
        path = ConstMapInfo.replace("\\", "/")
        splitPath = path.split("/")
        index = splitPath.index(PluginName)
        RelativePath = splitPath[index:]
        pathname = IPPath + "/".join(RelativePath)
        return pathname

    def save_to_path(self, save_path):
        """保存到文件"""
        with open(save_path, "w") as htmlFile:
            htmlFile.write(str(self.soup))

"""
（1） dir 一般表示文件夹，而不是路径，path 表示路径比较多
（2） 文本替换是什么文本替换，作用域是什么，对所有的文本进行替换吗？
（3）不必要的复杂结构，实现的东西比较简单就没必要用继承
"""

if __name__ =='__main__':

    inputHtmlDir = r'C:\Users\74722\Desktop\img\ARP_SO.html'
    outputHtmlDir = r'C:\Users\74722\Desktop\img\111.html'
    
    pictureDir = [r'C:\Users\74722\Desktop\aa.png',
                  r'C:\Users\74722\Desktop\aa.png',
                  r'C:\Users\74722\Desktop\aa.png',
                  r'C:\Users\74722\Desktop\aa.png',
                  r'C:\Users\74722\Desktop\aa.png',
                  r'C:\Users\74722\Desktop\aa.png']

    PluginName = "Anhui-html"
    keywords ={u"猜你喜欢": 'jokker'*100,"month":10}
    replace_key = 'table0'
    inputlist = [['淮北','江淮','江南'],['1','2','3'],['4','5','6'],['7','8','9']]


    # soup = textRplace(inputHtmlDir,outputHtmlDir,keywords)
    # soup.writeReport()

    soup = pictureFill(outputHtmlDir,outputHtmlDir,pictureDir,PluginName)
    soup.writeReport()
    #
    # soup =tableRplace(outputHtmlDir,outputHtmlDir,inputlist,replace_key)
    # soup.getTable()

    a = HtmlWrite(r'C:\Users\74722\Desktop\img\ARP_SO.html')
    a.txt_replace_in_assign_tag('a', {u"辞职报告": u'nono'*100 })
    a.save_to_path(r'C:\Users\74722\Desktop\img\112.html')
