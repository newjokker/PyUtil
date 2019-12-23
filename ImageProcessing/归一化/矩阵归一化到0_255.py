# -*- coding: utf-8  -*-
# -*- author: jokker -*-

# from scipy.misc import bytescale
from Function.GdalUtil import GdalBase
import numpy as np
from numpy import uint8


# FIXME scipy 包中的函数 from scipy.misc import bytescale
def bytescale(data, cmin=None, cmax=None, high=255, low=0):
    """
    Byte scales an array (image).

    Byte scaling means converting the input image to uint8 dtype and scaling
    the range to ``(low, high)`` (default 0-255).
    If the input image already has dtype uint8, no scaling is done.

    This function is only available if Python Imaging Library (PIL) is installed.

    Parameters
    ----------
    data : ndarray
        PIL image data array.
    cmin : scalar, optional
        Bias scaling of small values. Default is ``data.min()``.  # 设定数据的最小值， 如果有 -999 那么可以忽略这个值，直接写真实的最小值
    cmax : scalar, optional
        Bias scaling of large values. Default is ``data.max()``.  # 设定数据的最大值
    high : scalar, optional
        Scale max value to `high`.  Default is 255.  # 返回值的最大值
    low : scalar, optional
        Scale min value to `low`.  Default is 0.  # 返回值的最小值

    Returns
    -------
    img_array : uint8 ndarray
        The byte-scaled array.
    """

    if data.dtype == uint8:  # 当输入数据的类型是 uint8 的时候，就直接返回不做操作
        return data

    if high > 255:
        raise ValueError("`high` should be less than or equal to 255.")
    if low < 0:
        raise ValueError("`low` should be greater than or equal to 0.")
    if high < low:
        raise ValueError("`high` should be greater than or equal to `low`.")

    if cmin is None:
        cmin = data.min()
    if cmax is None:
        cmax = data.max()

    cscale = cmax - cmin
    if cscale < 0:
        raise ValueError("`cmax` should be larger than `cmin`.")
    elif cscale == 0:
        cscale = 1

    scale = float(high - low) / cscale
    bytedata = (data - cmin) * scale + low
    return (bytedata.clip(low, high) + 0.5).astype(uint8)  # 给定一个区间，该区间外的值被剪切到该区间，最后为什么要加 0.5 ？



tiff_path = r'D:\Code\FireDetectionH8\algorithm\AuxData\Landuse\land_use.tif'
im_data, im_width, im_height, im_bands, im_geotrans, im_proj = GdalBase.read_tiff(tiff_path)

im_data = im_data.astype(np.float)
a = bytescale(im_data, low=0, high=200)

print(np.unique(a))








