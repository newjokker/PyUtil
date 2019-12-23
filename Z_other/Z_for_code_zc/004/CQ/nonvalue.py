# -*- coding: utf-8 -*-
# author：ChenQiang 
# time:2019/12/5 0005

"""

"""

import LogUtil
from .Tool import *



# 测试数据准备
a = np.arange(25).reshape(5,5).astype(np.float)
a[a<3] = np.nan
a[a>21] = np.inf
print(a)
# np.inf,或者-np.inf(正负无穷大的数字)用有限数替代
print(np.nan_to_num(a))

b = np.arange(25).reshape(5,5).astype(np.float)
b[0,0] = np.inf
print(a[0,0],a[1,1],a[4,3],a[4,4])

if a[0,0] == a[1,1]:
    print('nan值相等')
else:
    print('nan值不相等')

if a[4,3] == a[4,4]:
    print('inf值相等')
else:
    print('inf值不相等')

inf_tif = r'E:\DEMO\ACheck\防风固沙功能\江苏固沙2015.tif'
[xsize,ysize,geotransform,geoproj,gtif,gband] = readFile(inf_tif)
# https://docs.scipy.org/doc/numpy/reference/generated/numpy.isfinite.html


# 各无效值间运算的结果
## inf
print(a[4,3]*(-1)) # inf有正负，inf与常量乘除
print(a[4,3]*(-1) + 10**100) # inf与常量加减
print(a[4,3] / b[0,0]) # inf与inf乘除 ==> nan
print(a[4,3] + b[0,0]) # inf与inf加减 ==> 同号：inf
print((a[4,3]*-1) + b[0,0]) # inf与inf加减 ==> 异号：nan

## nan
print(type(np.nan)) # np.nan是float类型，但是在进行int转换的时候就会报错
print(a[0,0] - a[4,3]) # nan +-*/ inf ==>nan
print(a[0,0] * a[1,1]) # nan +-*/ constant ==> nan
print(a[0,0] * 33) # nan +-*/ constant ==> nan

## NAN的不可比较性
print(a)
a[a>10] = 99
a[a<=10] = -99
## np.select
a = np.select([a>10,a<=10], [99,-99], default=0)


# 去除 np.
a[np.isnan(a)] = 0 # np.nan_to_num(),np.nanmax,np.nanmen……
a[np.isinf(a)] = 0



# ------------------产品
orgname = "INPUT.tif"
writefilename = "OUTPUT.tif"


[xsize,ysize,geotransform,geoproj,gtif,gband] = readFile(orgname)
np.isfinite(gtif)

# 获取无效值
print(gband.GetNoDataValue())
# 设置无效值
gband.SetNoDataValue(1000)
print(gband.GetNoDataValue())


# 设置取值范围
gtif[gtif>28508] = 28508


# TODO gtif[gtif==28508] = np.nan # 数据类型错误！！！
gtif_float = gtif.astype(np.float)
gtif_float[gtif_float==28508] = np.nan
# Or
# gtif[np.isnan(gtif)] = -9999


# 无效值的覆盖，NoDataValue是一个属性，在设置之后会覆盖之前的值
writeFile(writefilename,geotransform,geoproj,gtif_float,NoDataValue=2000)



print('!!!')



































