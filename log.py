import logging
import os
from concurrent_log_handler import ConcurrentRotatingFileHandler as RotatingFileHandler
import sys


class Log:
    def __init__(self, log_path=None, name=None):
        # 0 - 50
        self.log_mapping = {'notset': logging.NOTSET,
                            'debug': logging.DEBUG,
                            'info': logging.INFO,
                            'warning': logging.WARNING,
                            'error': logging.ERROR,
                            'critical': logging.CRITICAL}

        self.log_config = {'notset': {'maxBytes': 1, 'backupCount': 1},
                           'debug': {'maxBytes': 1, 'backupCount': 1},
                           'info': {'maxBytes': 1, 'backupCount': 1},
                           'warning': {'maxBytes': 1, 'backupCount': 2},
                           'error': {'maxBytes': 5, 'backupCount': 5},
                           'critical': {'maxBytes': 5, 'backupCount': 5}}

        self.init_log_path(log_path)
        self.public_name = 'z' if not name else name

        # initial log container
        self.logs = {}

    def init_log_path(self, log_path=None):
        def helper():
            root = os.path.dirname(os.path.abspath(__file__))
            if root.find('pack') >= 0:
                root = os.getcwd()
            return root

        if not log_path:
            self.log_root = helper()
        elif log_path in {'logs', 'log'}:
            self.log_root = helper() + '/' + log_path
        else:
            if log_path.split('/')[-1].find('.') >= 0:
                self.log_root = os.path.dirname(log_path)
            else:
                self.log_root = log_path
            if self.log_root == '//':
                self.log_root = '/'
            if not self.log_root.endswith('/'):
                self.log_root += '/'
        if not os.path.exists(self.log_root):
            os.makedirs(self.log_root)
        print('Log root --->>> ', self.log_root)

    def init_config(self, name=None):
        base_format = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        if name not in self.logs:
            # 创建logger
            logger = logging.getLogger(str(self.log_mapping[name]))
            logger.setLevel(self.log_mapping[name])
            # 创建hander用于写日日志文件
            log_path = self.log_root + self.public_name + '_' + name + '.log'
            base_handler = RotatingFileHandler(log_path, maxBytes=1 * 1024 * 1024, backupCount=1)
            # 定义日志的输出格式
            base_handler.setFormatter(base_format)
            base_handler.setLevel(self.log_mapping[name])
            # 给logger添加hander
            logger.addHandler(base_handler)
            # critical level add console hander
            if name == 'critical':
                console_handler = logging.StreamHandler()
                console_handler.setLevel(self.log_mapping[name])
                console_format = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
                console_handler.setFormatter(console_format)
                logger.addHandler(console_handler)
            self.logs.update({name: logger})

    def update_config(self, name: str):
        name = name.lower()
        assert name in {'notset', 'debug', 'info', 'warning', 'error', 'critical'}, '日志等级不正确'
        self.init_config(name)

    def warning(self, msg):
        func_name = sys._getframe().f_code.co_name
        self.update_config(func_name)
        return self.logs[func_name].warning(msg)

    def error(self, msg):
        func_name = sys._getframe().f_code.co_name
        self.update_config(func_name)
        return self.logs[func_name].error(msg)

    def critical(self, msg):
        func_name = sys._getframe().f_code.co_name
        self.update_config(func_name)
        return self.logs[func_name].critical(msg)

    def debug(self, msg):
        func_name = sys._getframe().f_code.co_name
        self.update_config(func_name)
        return self.logs[func_name].debug(msg)

    def notset(self, msg):
        func_name = sys._getframe().f_code.co_name
        self.update_config(func_name)
        return self.logs[func_name].notset(msg)

    def info(self, msg):
        func_name = sys._getframe().f_code.co_name
        self.update_config(func_name)
        return self.logs[func_name].info(msg)

if __name__ == '__main__':
    log = Log(log_path='logs')
    print(log.logs)
    log.warning('111')
    log.warning('222')
    log.critical('!!!!')
