# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import numpy as np
import cv2
from skimage import io, data
import matplotlib.pyplot as plt


class ImageProcessingUtil(object):

    @staticmethod
    def sp_noise(image, prob):
        """添加椒盐噪声, prob:噪声比例"""
        image = image.copy()  # 取原矩阵的深拷贝

        prob = prob / 2.0  # 信噪比 ∈ （0,1）所以先除以 2
        thres = 1 - prob
        if thres < prob:
            thres, prob = prob, thres

        m, n = image.shape
        mask = np.random.rand(m, n)  # 返回与 image 通行列的随机数矩阵
        image[mask < prob] = 0
        image[mask > thres] = 255
        return image

    @staticmethod
    def gasuss_noise(image, mean=0, var=0.1):
        """ 添加高斯噪声, mean : 均值, var : 方差"""
        image = np.array(image / 255.0, dtype=float)  # 设置值域为 （0, 1）
        noise = np.random.normal(mean, var ** 0.5, image.shape)
        out = image + noise
        out = np.clip(out, 0, 1.0)
        out = np.uint8(out * 255)
        return out


if __name__ == '__main__':
    coins = data.coins()
    coins_sp = ImageProcessingUtil.sp_noise(coins, 0.1)
    coins_gasuss = ImageProcessingUtil.gasuss_noise(coins)

    plt.subplot(311), plt.imshow(coins, cmap='gray')
    plt.subplot(312), plt.imshow(coins_sp, cmap='gray')
    plt.subplot(313), plt.imshow(coins_gasuss, cmap='gray')
    plt.show()
