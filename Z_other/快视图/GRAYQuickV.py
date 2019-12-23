# -*- coding: utf-8 -*-
"""
@author: DYX
@file: GRAYQuickV.py
@time: 2019/06/24
"""

import cv2
import numpy as np
from skimage import exposure
from scipy.misc import bytescale

class GRAYQuickV:
	
	def __init__(self, band, picPath, gamma):
		self.band = band
		self.picPath = picPath
		self.gamma = gamma
	
	def doQuick(self):
		# 背景值索引---------------------------------------------------------
		index = np.where(self.band == self.band[0][0])
		
		# scale 数据变换0~255------------------------------------------------
		band_scale = bytescale(self.band)
		band_scale = 255 - band_scale
		
		#自适应直方图均衡化--------------------------------------------------
		clahe = cv2.createCLAHE(clipLimit=5.0, tileGridSize=(10, 10))
		band_claheB = clahe.apply(np.array(band_scale, dtype=np.uint8))
		# band_claheB = cv2.equalizeHist(band_scale)
		
		# gamma调整   >1 变暗， <1变亮--------------------------------------
		band_claheB[band_claheB < 0] = 255
		gamma = float(self.gamma)
		b_gamma = exposure.adjust_gamma(band_claheB, gamma)
		
		# 傅里叶变换-------------------------------------------------------
		dft = cv2.dft(np.float32(b_gamma), flags=cv2.DFT_COMPLEX_OUTPUT)
		dftshift = np.fft.fftshift(dft)
		ishift = np.fft.ifftshift(dftshift)
		iimg = cv2.idft(ishift)
		shiftimg = cv2.magnitude(iimg[:, :, 0], iimg[:, :, 1])
		img = bytescale(shiftimg)
		
		# 背景设置白色---------------------------------------------------
		img[index] = 255
		b = img
		g = img
		r = img
		alpha_channel = np.ones(img.shape, dtype=img.dtype) * 255
		alpha_channel[index] = 0
		imgn = cv2.merge((b, g, r, alpha_channel))
		cv2.imwrite(self.picPath, imgn, [int(cv2.IMWRITE_JPEG_QUALITY), 70])