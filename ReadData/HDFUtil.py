# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import numpy as np
from pyhdf.SD import SD

# FIXME 可以使用 gdal 中的 wrap 方法来读取数据


def read_hdf_data(hdf_filepath, dataset, band):
    """1km MOD02数据，读取b1, b2, b5波段"""

    # 查看dataset数目及名字
    hdfObj = SD(hdf_filepath)
    # datasets_dic = hdfObj.datasets()
    # for idx, sds in enumerate(datasets_dic.keys()):
    #     print(idx, sds)

    EV_Aggr1km_RefSB = hdfObj.select(dataset)

    # 波段信息
    data = EV_Aggr1km_RefSB.get()[band]
    reflectance_scales = EV_Aggr1km_RefSB.attributes()['reflectance_scales'][band]
    reflectance_offsets = EV_Aggr1km_RefSB.attributes()['reflectance_offsets'][band]
    radiance_scales = EV_Aggr1km_RefSB.attributes()['radiance_scales'][band]
    radiance_offsets = EV_Aggr1km_RefSB.attributes()['radiance_offsets'][band]

    # 无效值
    fillvalue = 65535
    bandAry = data.astype(np.float)
    bandAry[np.where(bandAry == fillvalue)] = np.nan

    return bandAry, reflectance_scales, reflectance_offsets, radiance_scales, radiance_offsets
