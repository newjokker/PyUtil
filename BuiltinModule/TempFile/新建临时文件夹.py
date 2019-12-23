# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import time
import os
from tempfile import TemporaryDirectory

# ---------------------------------------------------------------------------------------------
# 指定（1）生成的文件夹（2）前缀
temp_folder = TemporaryDirectory(dir=r'C:\Users\Administrator\Desktop\del\del',
                                 prefix='jokker_')
print(temp_folder.name)
# time.sleep(10)

# 删除临时文件夹, fixme 如果文件被占用不会被删掉，会报错，这个要想办法解决
temp_folder.cleanup()
# ---------------------------------------------------------------------------------------------
# 书上建议的用法
with TemporaryDirectory() as dir_name:
    print(dir_name)

    with open(os.path.join(dir_name, 'test.txt'), 'w') as txt_file:
        for i in range(10):
            txt_file.write(str(i))

    time.sleep(30)

    with open(os.path.join(dir_name, 'test.txt'), 'r') as txt_file:
        for i in txt_file:
            print(i)

