# -*- coding: utf-8  -*-
# -*- author: jokker -*-

from Report.LoadUtil import LoadUtil

VNP_url = r'https://firms.modaps.eosdis.nasa.gov/data/active_fire/viirs/shapes/zips/VNP14IMGTDL_NRT_Russia_and_Asia_24h.zip'
save_path = r'C:\Users\Administrator\Desktop\del\del_ningan\123.zip'


LoadUtil.load_file_from_url(VNP_url, save_path)

