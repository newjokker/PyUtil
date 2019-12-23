# -*- coding: utf-8  -*-
# -*- author: jokker -*-


"""
有使用（1）Arcpy 和 （2） .exe 两种方法
"""

import arcpy

def grid_to_tiff(grb2_path, out_grb2_tif_path):
    """grid 转为 tiff"""
    # arcpy.env.workspace = r"C:/Workspace"
    arcpy.ExtractSubDataset_management(grb2_path, out_grb2_tif_path)

