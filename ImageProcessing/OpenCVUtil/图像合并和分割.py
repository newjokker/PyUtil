# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import cv2

(bL, gL, rL) = cv2.split(img_LAB)  # 图像分割

img_clahe = cv2.merge((claheB, gL, rL))  # 图像合并

