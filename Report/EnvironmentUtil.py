# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import warnings


# numpy 设置不通知 : np.seterr(divide='ignore', invalid='ignore')


class EnvironmentUtil(object):

    @staticmethod
    def warning(action='ignore'):
        """设置"""
        warnings.filterwarnings(action=action)

    @staticmethod
    def clear_mode():
        """干净模式，去掉那些不需要的显示内容"""
        # 去掉 worning 报错
        EnvironmentUtil.warning()
        pass