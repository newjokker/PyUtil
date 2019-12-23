# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import arcpy

@staticmethod
def clearWorkSpace():
    '''
    重置工作空间
    '''
    arcpy.ClearEnvironment("workspace")
    arcpy.ResetEnvironments()

    arcpy.Delete_management()  # 使用这个删除干净


