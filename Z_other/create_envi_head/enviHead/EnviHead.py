# -*- coding: utf-8  -*-
# -*- author: jokker -*-

def add_head_file(self, tiff_name, band_file_names):
    """新增头文件"""

    head_model_file_path = r'D:\Code\Util_Util\Z_other\head\enviHead\head_model.hdr'
    im_data, im_width, im_height, im_bands, im_geotrans, im_proj = GdalBase.read_tiff(tiff_name)
    # --------------------------------------------------------------------------------------------
    with open(head_model_file_path, 'r') as head_file:
        model_str = ''.join(head_file.readlines())
        new_band_names = map(lambda x:os.path.basename(x), band_file_names)
        model_str = model_str.format(im_width, im_height, im_bands, ','.join(new_band_names))
        model_str = model_str.replace('[', '{')
        model_str = model_str.replace(']', '}')
    # --------------------------------------------------------------------------------------------
    head_file_path = tiff_name[:-4] + '.hdr'  # hdr 文件名
    # --------------------------------------------------------------------------------------------
    with open(head_file_path, 'w') as head_file:
        head_file.write(model_str)

