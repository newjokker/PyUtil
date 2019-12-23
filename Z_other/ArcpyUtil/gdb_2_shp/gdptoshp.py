# -*- coding:gbk -*-
import arcpy, os
from arcpy import env


def Merge(inputgdb,outputshp):
    '''

    :param inputgdb:
    :param outputshp:
    :return:
    '''
    lspt = []
    for i in os.listdir(inputgdb):
        lspt.append(os.path.join(inputgdb, i, xianzhi + ".shp"))
    arcpy.Merge_management(lspt, outputshp)

def organize_data(inputfolder,outputfolder,condition):
    '''

    :param inputfolder:
    :param outputfolder:
    :param condition:
    :return:
    '''
    for r, ds, fs in os.walk(inputfolder):
        newpath = r.replace(inputfolder, outputfolder)
        if not os.path.exists(newpath):
            os.mkdir(newpath) #路径下gdb不存在则创建gdb
        if r[-4:] == ".gdb":
            env.workspace = r
            gdbpath = r.replace(inputfolder, outputfolder)
            print mdbpath
            gdbtoshp(gdbpath,condition)

def gdbtoshp(outfolder,condition):
    '''

    :param outfolder:
    :param condition:
    :return:
    '''
    fcs = arcpy.ListFeatureClasses()
    for fc in fcs:
        if fc==condition:
            arcpy.CopyFeatures_management(fc, outfolder + os.sep + str(fc))
            print fc

if __name__ == "__main__":

    inputfolder = r'D:\GanSu\1比100万China边界(含县级河流)国家测绘局2\1比100万China边界(含县级河流)国家测绘局2'
    outputgdbfolder = r"D:/GanSu/shp/china.gdb"
    outputshp = r"D:\GanSu\shp\china.shp"
    xianzhi = u"BOUA"

    organize_data(inputfolder,outputgdbfolder,xianzhi)
    Merge(outputgdbfolder,outputshp)



    # tempshp = r"D:\Fujian\China_CGCS2000.shp"
    #
    # inputshp = r"D:\GanSu\shp\china_province.shp"
    #
    # rows1 = arcpy.SearchCursor(inputshp)  # 读取属性表
    #
    # pac = 'PAC'
    # n_pac = 'N_PAC'
    # p_pac = 'P_PAC'
    # c_pac = 'C_PAC'
    # x_pac = 'X_PAC'
    # P_PAC_list = []
    # # for row in rows1:
    # #
    # #     item = row.getValue(pac)
    # #     if item!= 156:
    # #         P_PAC_list.append(str(item)[:2]+'0000000000')
    # #     else:
    # #         P_PAC_list.append("000000000000")
    # # p_v = {}
    # #
    # # for row in rows1:
    # #
    # #     item = row.getValue("P_PAC")
    # #     for province in p_v:
    # #         if item == province:
    # #             P_PAC_list.append(province)
    #
    #
    # cursor = arcpy.UpdateCursor(tempshp)
    # # arcpy.AddField_management(inputshp, "P_NAME", "TEXT")
    # i = 0
    # for my_row in cursor:
    #     my_value = my_row.getValue(n_pac)
    #     my_row.setValue(n_pac, '000000000000')
    #     cursor.updateRow(my_row)
    #     i += 1
