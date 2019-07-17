import logging
from logging.handlers import RotatingFileHandler
import os

"""
2019-07-09  
新版日志模块，试用版！
"""


class Log:
    def __init__(self, path=None,
                 warning_size: int = 1, warning_backup_num: int = 2, warning_notice: str = None,
                 error_size: int = 10, error_backup_num: int = 5, error_notice: str = None,
                 critical_size: int = 5, critical_backup_num: int = 2, critical_notice: str = None):
        """

        :param warning_size:            warning等级单个文件上限大小（MB）
        :param warning_backup_num:      warning等级备份文件个数
        :param warning_notice:          warning等级日志文件后缀
        :param error_size:              error等级单个文件上限大小（MB）
        :param error_backup_num:        error等级备份文件个数
        :param error_notice:            error等级日志文件后缀
        :param critical_size:           critical等级单个文件上限大小（MB）
        :param critical_backup_num:     critical等级备份文件个数
        :param critical_notice:         critical等级日志文件后缀
        """

        # 方便查看和统一文件，默认使用z开头
        self.head = 'z'

        # 日志文件路径
        if not path:
            path = os.path.dirname(os.path.abspath(__file__)) + '/'
            if path.find('pack') >= 0:
                path = os.getcwd() + '/'
        self.path = path

        # 设置50级别的日志打印出控制台
        self.console = logging.StreamHandler()
        self.console.setLevel(50)
        consoleFormat = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        self.console.setFormatter(consoleFormat)

        # 新建过滤器对象
        self.infoFilter = logging.Filter()
        self.debugFilter = logging.Filter()
        self.warningFilter = logging.Filter()
        self.errorFilter = logging.Filter()
        self.criticalFilter = logging.Filter()

        # 设置日志等级
        self.infoFilter.filter = lambda level: 20 <= level.levelno <= 20
        self.debugFilter.filter = lambda level: 10 <= level.levelno <= 10
        self.warningFilter.filter = lambda level: 30 <= level.levelno <= 30
        self.errorFilter.filter = lambda level: 40 <= level.levelno <= 40
        self.criticalFilter.filter = lambda level: 50 <= level.levelno <= 50

        self.init_warning(notice=warning_notice, size=warning_size, backup_num=warning_backup_num)
        self.init_error(notice=error_notice, size=error_size, backup_num=error_backup_num)
        self.init_critical(notice=critical_notice, size=critical_size, backup_num=critical_backup_num)

    # 初始化配置
    def init_warning(self, notice: str = None, size: int = 1, backup_num: int = 2):
        if not notice:
            self.warningOperation = RotatingFileHandler(self.path + self.head + '_warning.log', maxBytes=size * 1024 * 1024, backupCount=backup_num)
        else:
            self.warningOperation = RotatingFileHandler(self.path + self.head + '_warning_%s.log' % notice, maxBytes=size * 1024 * 1024, backupCount=backup_num)
        self.warningOperation.addFilter(self.warningFilter)
        warningFormat = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        self.warningOperation.setFormatter(warningFormat)
        self.log_warning = logging.getLogger()
        self.log_warning.setLevel(logging.DEBUG)
        self.log_warning.addHandler(self.warningOperation)
        self.log_warning.addHandler(self.console)

    def init_error(self, notice: str = None, size: int = 10, backup_num: int = 5):
        if not notice:
            self.errorOperation = RotatingFileHandler(self.path + self.head + '_error.log', maxBytes=size * 1024 * 1024, backupCount=backup_num)
        else:
            self.errorOperation = RotatingFileHandler(self.path + self.head + '_error_%s.log' % notice, maxBytes=size * 1024 * 1024, backupCount=backup_num)
        self.errorOperation.addFilter(self.errorFilter)
        errorFormat = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        self.errorOperation.setFormatter(errorFormat)
        self.log_error = logging.getLogger()
        self.log_error.setLevel(logging.DEBUG)
        self.log_error.addHandler(self.errorOperation)
        self.log_error.addHandler(self.console)

    def init_critical(self, notice: str = None, size: int = 1, backup_num: int = 2):
        if not notice:
            self.criticalOperation = RotatingFileHandler(self.path + self.head + '_critical.log', maxBytes=size * 1024 * 1024, backupCount=backup_num)
        else:
            self.criticalOperation = RotatingFileHandler(self.path + self.head + '_critical_%s.log' % notice, maxBytes=size * 1024 * 1024, backupCount=backup_num)
        self.criticalOperation.addFilter(self.criticalFilter)
        criticalFormat = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        self.criticalOperation.setFormatter(criticalFormat)
        self.log_critical = logging.getLogger()
        self.log_critical.setLevel(logging.DEBUG)
        self.log_critical.addHandler(self.criticalOperation)
        self.log_critical.addHandler(self.console)

    @staticmethod
    def combine(msg: str,
                e: Exception = None):
        """

        :param msg:     自定义日志信息
        :param e:       错误信息e
        :return:
        """
        if not isinstance(msg, str):
            msg = str(msg)
        if e:
            content = 'File:' + str(e.__traceback__.tb_frame.f_code.co_filename) + '------Line:' + str(e.__traceback__.tb_lineno) + '------Error:' + str(e) + '------Tips:' + str(msg)
        else:
            content = msg
        return content

    def warning(self, msg, e=None, *args, **kwargs):
        """

        :param msg:         自定义日志信息
        :param e:           错误信息e
        :param notice:      文件后缀，一般用于区分同一个文件夹不同脚本的日志文件
        :param size:        日志文件大小，MB
        :param back_num:    备份回滚日志个数
        :param args:
        :param kwargs:
        :return:
        """
        content = self.combine(msg, e)

        return self.log_warning.warning(content, *args, **kwargs)

    def error(self, msg, e=None, *args, **kwargs):

        content = self.combine(msg, e)

        return self.log_error.error(content, *args, **kwargs)

    def critical(self, msg, e=None, *args, **kwargs):

        content = self.combine(msg, e)

        return self.log_critical.critical(content, *args, **kwargs)
