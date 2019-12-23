# -*- coding: utf-8  -*-
# -*- author: jokker -*-

# 参考 ： https://blog.csdn.net/jclian91/article/details/80628188

# 解决报错的问题 ：https://www.cnblogs.com/benson321/p/10502339.html

"""
图片清晰一点，识别率还是挺高的，可以将之前的段子找到，全部数字化
"""

import pytesseract
from PIL import Image


class OCRUtil(object):

    @staticmethod
    def get_words_from_image(img_path, lang='chi_sim', tesseract_cmd=None):
        """从图片中识别文字"""
        try:
            if tesseract_cmd is None:
                tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
            # text = pytesseract.image_to_string(Image.open(img_path), lang=lang)  # chinese
            text = pytesseract.image_to_string(Image.open(img_path))  # chinese
            return text
        except TypeError:
            return None


if __name__ == '__main__':

    Text = OCRUtil.get_words_from_image(r'C:\Users\Administrator\Desktop\a.jpg')

    print(Text)
