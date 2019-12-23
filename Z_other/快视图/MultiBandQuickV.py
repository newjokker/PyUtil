# -*- coding: utf-8 -*-
"""
@author: DYX
@file: MultiBandQuickV.py
@time: 2019/06/21
"""

import cv2
import numpy as np
import math
from skimage import exposure
from scipy.misc import bytescale

class MultiBandQuickV:
	
	def __init__(self, band1, band2, band3, picPath, gamma):
		self.b = band1
		self.g = band2
		self.r = band3
		self.picPath = picPath
		self.gamma = gamma
	
	def doQuick(self):
		# -------------------获取背景值索引
		index = np.where(self.b == self.b[0][0])
		
		self.b[index] = 0.
		self.g[index] = 0.
		self.r[index] = 0.
		
		# -------------------重采样
		srcX = self.b.shape[0]
		srcY = self.b.shape[1]
		
		dstY, dstX = int(math.ceil(srcX / 1)), int(math.ceil(srcY / 1))         # 后续调整：不在做重采样，所以scale=1
		
		# b_resize = cv2.resize(self.b, (dstX, dstY), interpolation=cv2.INTER_AREA)
		# g_resize = cv2.resize(self.g, (dstX, dstY), interpolation=cv2.INTER_AREA)
		# r_resize = cv2.resize(self.r, (dstX, dstY), interpolation=cv2.INTER_AREA)
		b_resize = self.b
		g_resize = self.g
		r_resize = self.r
		
		# ------------------scale 转换为0~255
		b_scale = bytescale(b_resize)
		g_scale = bytescale(g_resize)
		r_scale = bytescale(r_resize)

		# FIXME 自适应直方图均衡化，保持各个区域亮度均一
		img_scale = cv2.merge((b_scale, g_scale, r_scale))
		img_LAB = cv2.cvtColor(img_scale, cv2.COLOR_BGR2LAB)
		(bL, gL, rL) = cv2.split(img_LAB)  # 亮度，从红色到绿色的范围，从黄色到蓝色的范围，
		clahe = cv2.createCLAHE(clipLimit=5.0, tileGridSize=(10, 10))
		claheB = clahe.apply(np.array(bL, dtype=np.uint8))  # FIXME 这里用直方图均衡化让各个地方的亮度保持均衡，
		img_clahe = cv2.merge((claheB, gL, rL))
		imgColor = cv2.cvtColor(img_clahe, cv2.COLOR_LAB2BGR)

		# FIXME 调整整体的亮度
		gamma = float(self.gamma)
		imgColor_gamma = exposure.adjust_gamma(imgColor, gamma)
		
		# 设置透明, FIXME 这边不是设置透明，这边是设置背景
		(bC, gC, rC) = cv2.split(imgColor_gamma)
		bC[index] = 255
		gC[index] = 255
		rC[index] = 255
		
		alpha_channel = np.ones(bC.shape, dtype=bC.dtype) * 255
		img = cv2.merge((bC, gC, rC, alpha_channel))
		# img = cv2.merge((bC, gC, rC))
		
		cv2.imwrite(self.picPath, img, [int(cv2.IMWRITE_JPEG_QUALITY), 70])


if __name__ == '__main__':

	pass


