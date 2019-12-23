# -*- coding: utf-8  -*-
# -*- author: jokker -*-

from FireProcess.AuxData.fire_process import FireMonitorProcessH8
import pickle

def H8_data_pretreatment(self):
    """预处理"""
    # 通过白天黑夜决定波段，若是黑夜，则1,2,3不做预处理;3,4,7,14处理为2KM分辨率,白天额外处理1,2,3波段，出成500M
    self.pre_data_dict = FireMonitorProcessH8.pretreatment(
        self.file_time, self.channals, self.segments, self.extend, self.pixSize, self.input_data_dir,
        self.out_pre_pro_path, self.temp_path)

    # 是否保留 pkl 文件
    if self.save_pretreatment_pkl:
        # 将预处理的结果生成 pkl 文件保存在本地
        pre_result_folder = os.path.join(self.out_dir, r'pre_data_dict')

        # 存放 pkl 文件的文件夹
        if not os.path.exists(pre_result_folder):
            os.makedirs(pre_result_folder)

        # pkl 文件路径
        pre_result_pkl = os.path.join(pre_result_folder, 'pre_result_{0}.pkl'.format(self.file_time))
        with open(pre_result_pkl, 'wb') as pkl_file:
            pickle.dump(self.pre_data_dict, pkl_file)