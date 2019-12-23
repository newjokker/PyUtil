# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import cv2

img_scale = cv2.merge((b_scale, g_scale, r_scale))
img_LAB = cv2.cvtColor(img_scale, cv2.COLOR_BGR2LAB)  # RGB ==> LAB

img_clahe = cv2.merge((claheB, gL, rL))
imgColor = cv2.cvtColor(img_clahe, cv2.COLOR_LAB2BGR)  # LAB ==> RGB

