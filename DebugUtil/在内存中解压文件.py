# -*- coding: utf-8  -*-
# -*- author: jokker -*-



# -------------------- 内存中处理压缩文件 -------------------------

import requests
import tarfile
import zipfile
from io import BytesIO

url = "https://firms.modaps.eosdis.nasa.gov/data/active_fire/c6/shapes/zips/MODIS_C6_Russia_and_Asia_24h.zip"   # the url you get tar.bz2 file from, need to change according to your application.
filename = "res_test.csv"  # the filename in your tar.bz2 file.


def decompress_tar_bz2_from_net(url, filename):
    """
    decompress the tar.bz2 format file in memory, instead of buffer it on disk
    and then decompress.
    :param url:
    :param filename:
    :return:
    """
    fileobj = BytesIO(requests.get(url).content)
    contents = tarfile.open(fileobj=fileobj).extractfile(filename).read()

    return contents


if __name__ == '__main__':

    # fixme 未成功，查看原因

    decompress_tar_bz2_from_net(url, filename)
