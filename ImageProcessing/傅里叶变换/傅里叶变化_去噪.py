# -*- coding: utf-8  -*-
# -*- author: jokker -*-

from scipy import fftpack
from skimage import data, io
import numpy as np
import matplotlib.pyplot as plt
from ImageProcessing.ImageProcessingUtil import ImageProcessingUtil


img_old = data.coins()  # 载入图像
# img_old = io.imread(r'C:\Users\Administrator\Desktop\timg.jpg')[:,:,0]

img = ImageProcessingUtil.sp_noise(img_old, 0.05)

# 加了噪音的图像转频率域
F = fftpack.fftn(img)
F_magnitude = np.abs(F)
F_magnitude = fftpack.fftshift(F_magnitude)

# 原始图像转频率域
F_old = fftpack.fftn(img_old)
F_magnitude_old = np.abs(F_old)
F_magnitude_old = fftpack.fftshift(F_magnitude_old)

# 将频谱中心的一块区域归零
M, N = img.shape
K = 20
F_magnitude[M//2 - K: M//2+K, N//2 - K: N//2 + K] = 0

#
peaks = F_magnitude < np.percentile(F_magnitude, 98)  # 找到非峰值的区域
peaks = fftpack.ifftshift(peaks)  # 将峰值平移回去，靠近原来的频谱
F_dim = F.copy()  # 复制一个原始（复数）频谱的副本
F_dim = F_dim * peaks.astype(int)  # 将这些峰值的系数设置为 0
image_filtered = np.real(fftpack.ifft2(F_dim))


# 显示频谱时，需要取对数压缩值域
plt.subplot(321), plt.imshow(np.log(1+F_magnitude_old), cmap='gray')  # 使用对数压缩，显示
plt.subplot(322), plt.imshow(np.log(1+F_magnitude), cmap='gray')
plt.subplot(323), plt.imshow(img_old, cmap='gray')
plt.subplot(324), plt.imshow(img, cmap='gray')
plt.subplot(325), plt.imshow(image_filtered, cmap='gray')

plt.show()





