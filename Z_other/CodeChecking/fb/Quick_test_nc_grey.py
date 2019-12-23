# -*- coding: utf-8 -*-

import numpy as np
from scipy.misc import bytescale
import gdal
import cv2
from skimage import exposure


class Quick_grey:

    def __init__(self, dir,filePath):
        self.dir = dir
        self.filePath = filePath

    def quick_grey(self):
        tiffile = self.filePath
        dstfile = self.dir +r'\workspace\outfile\test.png'
        ds = gdal.Open(tiffile)
        data = ds.GetRasterBand(1).ReadAsArray()
        bgValue = data[0][0]
        index = np.where(data == bgValue)
        index_t = np.where(data != bgValue)
        bgValue_min=min(data[index_t])
        data[index] = bgValue_min

        index = np.where(data == bgValue)
        new_data = bytescale(data)
        new_data = 255 - new_data

        clahe = cv2.createCLAHE(clipLimit=5.0, tileGridSize=(10, 10))
        band_claheB = clahe.apply(np.array(new_data, dtype=np.uint8))

        # gamma调整   >1 变暗， <1变亮
        band_claheB[band_claheB < 0] = 255
        gamma = float(0.7)
        b_gamma = exposure.adjust_gamma(band_claheB, gamma)

        # 傅里叶变换
        dft = cv2.dft(np.float32(b_gamma), flags=cv2.DFT_COMPLEX_OUTPUT)
        dftshift = np.fft.fftshift(dft)
        ishift = np.fft.ifftshift(dftshift)
        iimg = cv2.idft(ishift)
        shiftimg = cv2.magnitude(iimg[:, :, 0], iimg[:, :, 1])

        img = bytescale(shiftimg)

        #替换背景值
        img[index] = 255
        b = img
        g = img
        r = img
        alpha_channel = np.ones(img.shape, dtype=img.dtype) * 255
        alpha_channel[index] = 0
        imgn = cv2.merge((b, g, r, alpha_channel))
        cv2.imwrite(dstfile, imgn, [int(cv2.IMWRITE_JPEG_QUALITY), 80])

