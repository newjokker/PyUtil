# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import cv2
import numpy as np
from scipy.misc import bytescale
from matplotlib import pyplot as plt

b_gamma = cv2.imread(r'C:\Users\Administrator\Desktop\aaa.jpg')[:,:,0]

# FIXME 傅里叶变换
dft = cv2.dft(np.float32(b_gamma), flags=cv2.DFT_COMPLEX_OUTPUT)  # dtf() ：对一维或者二维浮点数数组进行正向或反向傅里叶变换
dftshift = np.fft.fftshift(dft)  # 图像转为频率与图像，就是中间点向外发散的图像
ishift = np.fft.ifftshift(dftshift)
iimg = cv2.idft(ishift)
shiftimg = cv2.magnitude(iimg[:, :, 0], iimg[:, :, 1])  # 计算由 x y 频率域得到的 二维上的 综合频率域分布？

img = bytescale(shiftimg)

# 出图，正常图像和映射到频率域的图像
magnitude_spectrum = 20*np.log(cv2.magnitude(dftshift[:,:,0],dftshift[:,:,1]))
plt.subplot(221),plt.imshow(img, cmap = 'gray')
plt.title('Input Image'), plt.xticks([]), plt.yticks([])
plt.subplot(222),plt.imshow(magnitude_spectrum, cmap = 'gray')
plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
magnitude_spectrum_x = dftshift[:,:,0]
plt.subplot(223),plt.imshow(magnitude_spectrum_x, cmap = 'gray')
magnitude_spectrum_y = dftshift[:,:,1]*10
plt.subplot(224),plt.imshow(magnitude_spectrum_y, cmap = 'gray')
plt.show()



cv2.imwrite(r'C:\Users\Administrator\Desktop\after.jpg', img)
cv2.imwrite(r'C:\Users\Administrator\Desktop\before.jpg', b_gamma)


# FIXME  傅里叶变换不但可以去噪，还能对图像进行校正，https://blog.csdn.net/wsp_1138886114/article/details/83374333

