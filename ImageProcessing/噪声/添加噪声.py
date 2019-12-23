# -*- coding: utf-8  -*-
# -*- author: jokker -*-


import numpy as np
import random
import cv2
from skimage import io, data
import matplotlib.pyplot as plt

def sp_noise(image,prob):
    '''
    添加椒盐噪声
    prob:噪声比例
    '''
    output = np.zeros(image.shape,np.uint8)
    thres = 1 - prob
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = random.random()
            if rdn < prob:
                output[i][j] = 0
            elif rdn > thres:
                output[i][j] = 255
            else:
                output[i][j] = image[i][j]
    return output

def gasuss_noise(image, mean=0, var=0.1):
    '''
        添加高斯噪声
        mean : 均值
        var : 方差
    '''
    image = np.array(image/255. , dtype=float)
    noise = np.random.normal(mean, var ** 0.5, image.shape)
    out = image + noise
    if out.min() < 0:
        low_clip = -1.
    else:
        low_clip = 0.
    out = np.clip(out, low_clip, 1.0)
    out = np.uint8(out*255)
    #cv.imshow("gasuss", out)
    return out


if __name__ == '__main__':

    coins = data.coins()
    coins_sp = sp_noise(coins, 0.0001)
    coins_gasuss = gasuss_noise(coins)

    plt.subplot(311), plt.imshow(coins, cmap='gray')
    plt.subplot(312), plt.imshow(coins_sp, cmap='gray')
    plt.subplot(313), plt.imshow(coins_gasuss, cmap='gray')
    plt.show()



