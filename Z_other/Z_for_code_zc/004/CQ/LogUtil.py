# -*- coding: utf-8 -*-
import os
import threading
import logging
from logging.handlers import RotatingFileHandler
# import configparser # py3
import ConfigParser

# FIXME 不同模块层级间调用有问题

class LogSignleton(object):

    def __init__(self, log_conf, log_file):
        pass

    def __new__(cls, log_conf, log_file):
        # self.aux_dir + __LogConf__, log_file=self.aux_dir + __LogFile__

        mutex = threading.Lock()
        mutex.acquire()  # 上锁，防止多线程下出问题

        if not hasattr(cls, 'instance'):
            cls.instance = super(LogSignleton, cls).__new__(cls)
            # config = configparser.ConfigParser()  # py3
            config = ConfigParser.ConfigParser()
            if log_conf is None:
                print('First init need set log_config file path')
            config.read(log_conf)
            if log_conf is None:
                cls.instance.log_filename = config.get('LOGGING', 'log_file')
            else:
                cls.instance.log_filename = log_file
            cls.instance.max_bytes_each = int(config.get('LOGGING', 'max_bytes_each'))
            cls.instance.backup_count = int(config.get('LOGGING', 'backup_count'))
            cls.instance.fmt = config.get('LOGGING', 'fmt')
            cls.instance.log_level_in_console = int(config.get('LOGGING', 'log_level_in_console'))
            cls.instance.log_level_in_logfile = int(config.get('LOGGING', 'log_level_in_logfile'))
            cls.instance.logger_name = config.get('LOGGING', 'logger_name')
            # cls.instance.logger_name = os.path.basename(__file__)[:-3]
            cls.instance.console_log_on = int(config.get('LOGGING', 'console_log_on'))
            cls.instance.logfile_log_on = int(config.get('LOGGING', 'logfile_log_on'))
            cls.instance.logger = logging.getLogger(cls.instance.logger_name)
            cls.instance.__config_logger()
        mutex.release()
        return cls.instance

    def get_logger(self):
        return self.logger

    def __config_logger(self):

        # 设置日志格式
        # self.logger.handlers.clear()  # CNQ
        fmt = self.fmt.replace('|', '%')
        formatter = logging.Formatter(fmt)
        if self.console_log_on == 1:  # 如果开启控制台日志
            console = logging.StreamHandler()
            # console.setLevel(self.log_level_in_console)
            console.setFormatter(formatter)
            self.logger.addHandler(console)
            self.logger.setLevel(self.log_level_in_console)
            # # 在使用完console后从移除Handler
            # self.logger.removeHandler(console)

        if self.logfile_log_on == 1:  # 如果开启文件日志
            rt_file_handler = RotatingFileHandler(self.log_filename, maxBytes=self.max_bytes_each,
                backupCount=self.backup_count)
            rt_file_handler.setFormatter(formatter)
            self.logger.addHandler(rt_file_handler)
            self.logger.setLevel(self.log_level_in_logfile)
            # # 在使用完rt_file_handler后从移除Handler
            # self.logger.removeHandler(rt_file_handler)


if __name__ == '__main__':
    logsignleton = LogSignleton(r'E:\FIRE\FireDetectionH8\AuxData\Log\FireLog.conf', log_file = r'E:\FIRE\FireDetectionH8\AuxData\test.log' )

    logger = logsignleton.get_logger()

    logger1 = logsignleton.get_logger()

    print(id(logger) == id(logger1))

    # logger = logging.getLogger('test_logger') # 在其它模块中时，可这样获取该日志实例

    logger.debug('this is a debug level message')

    logger.info('this is info level message')

    logger.warning('this is warning level message')

    logger.error('this is error level message')

    logger.critical('this is critical level message')