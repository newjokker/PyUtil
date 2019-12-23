# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import os
import py_compile

"""
* 将一个目录下的所有文件都编译，然后删除对应的 py 文件
* 对于 Python3 因为有了新的组织方式，所以需要进行对应的改动
"""


class CompileUtil(object):

    @staticmethod
    def find_all_py_in_folder(folder_path):
        """找到文件夹中的所有 py 文件"""
        py_files = list()
        for i, j, k in os.walk(folder_path):
            for file_py in k:
                if file_py.endswith('.py'):
                    py_path_temp = os.path.join(i, file_py)
                    py_files.append(py_path_temp)
        return py_files

    @staticmethod
    def compile_and_del(py_files):
        """编译和删除 py 文件"""
        # 对 py 文件进行编译
        for each_py_file in py_files:
            py_compile.compile(each_py_file)

        # 删除编译后的 py 文件
        for each_py_file in py_files:
            os.remove(each_py_file)

    @staticmethod
    def do_compile_for_dir(folder_path):
        """对某一个文件夹进行编译操作？（这样解释似乎不合适）"""
        try:
            # 找到 py 文件
            py_files = CompileUtil.find_all_py_in_folder(folder_path)
            # 编译和删除 py 文件
            CompileUtil.compile_and_del(py_files)
            print('compile for {} file'.format(len(py_files)))
            return True
        except:
            return False


if __name__ == '__main__':

    folderPath = r'C:\Users\Administrator\Desktop\util_test'
    print(CompileUtil.do_compile_for_dir(folderPath))

