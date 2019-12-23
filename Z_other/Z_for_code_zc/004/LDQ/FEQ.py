# -*- coding: utf-8  -*-
# -*- author: jokker -*-

"""
植被覆盖状况,VCS(√)
植被生长状况,VGS(√)
植被质量状况,VQS(*)
森林生态系统质量,FEQ(√)
草地生态系统质量,GEQ(√)
"""


class FEQ(BaseProcess):
    """景观相关参数"""

    def doStatisComp(self, tempDir, tifPath, minAreaShp, levelArea, curProNumber):
        """统计分析"""
        initStaMap = self.doStatisInit()
        # --------------------------------------------------------------------------------------------------------------
        # #【1】统计，【临时文件夹，tif文件，最小的行政区划，区域的等级】，无需返回值
        # 【jokker】这边指定特殊的分级
        if len(self.pluginParam.getInputInfoByKey('assignGrade').split(',')) == 4:
            # assign_grade = [0.5, 1.5, 2.5, 3.5]
            assign_grade = [i+0.5 for i in range(4)]
        elif len(self.pluginParam.getInputInfoByKey('assignGrade').split(',')) == 6:
            assign_grade = [i+0.5 for i in range(6)]
        else:
            raise ValueError('assign grade can only be 3 class or 5 class')
        #
        new_grade = {}
        for i in range(len(assign_grade)-1):
            key_temp = 'VALUE >= {0} and VALUE < {1}'.format(assign_grade[i], assign_grade[i+1])
            new_grade[key_temp] = i
        # 直接改变私有变量
        self.pluginParam._ProductInfo__reMapAry = new_grade
        self.areaStatis(tempDir, tifPath, minAreaShp, levelArea, ConstParam.ALLSTATISTICS)
        # --------------------------------------------------------------------------------------------------------------
        # 【2】专题图
        depand_folder = self.pluginParam.getDependFolder()
        if len(self.pluginParam.getInputInfoByKey('assignGrade').split(',')) == 4:
            self.pluginParam.setDependFolder(os.path.join(depand_folder, 'mxd', 'FEQ', 'class_3'))
        elif len(self.pluginParam.getInputInfoByKey('assignGrade').split(',')) == 6:
            self.pluginParam.setDependFolder(os.path.join(depand_folder, 'mxd', 'FEQ', 'class_5'))
        else:
            raise ValueError('assign grade can only be 3 class or 5 class')
        curProNumber = curProNumber + 2
        self.creatPic(tifPath, initStaMap, str(float('%.2f' % curProNumber)))
        self.pluginParam.setDependFolder(depand_folder)  # 将改变 depend 文件夹的影响修改过来
        # --------------------------------------------------------------------------------------------------------------
























