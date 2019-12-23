# -*- coding: utf-8  -*-
# -*- author: jokker -*-


import cv2
import numpy as np
from skimage import data
import matplotlib.pyplot as plt

img = data.jokker_happy()
img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)