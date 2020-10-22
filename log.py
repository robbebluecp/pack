import os
from concurrent_log_handler import ConcurrentRotatingFileHandler as RotatingFileHandler
from concurrent_log_handler import logging
import sys
import datetime, time
from pytz import timezone, utc


class Log:
    def __init__(self, name=None, log_path=None, gap=8):

        """
        This module designed for recording log files into your DIY path with your DIY prefix name.
        Including six builtin levels (notset, debug, info, warning, error ,critical) and each one
        will be added into class logs( type dict ) whenever you wish to call a log func. And if not
        called, the relative log file won't be recorded into log path.

        Default configurations(maxBytes and backupCount) is set with parameter log_config. Util now you have to inherit this
        class or just modify these parameters if you  want to change any configs. And more configs will be add in future.

        Here are some examples will show you how to use log to record log files:


        :param log_path:        path for record log files
        :param name:            log prefix name
        :param gap:             timezone diff from UTC to local timezone
                                For exmaple: if your location is Asia/Beijing, then gap should be 8 (GTM + 8)
        """
        # 0 - 50
        self.log_mapping = {'notset': logging.NOTSET,
                            'debug': logging.DEBUG,
                            'info': logging.INFO,
                            'warning': logging.WARNING,
                            'error': logging.ERROR,
                            'critical': logging.CRITICAL}

        # log basic config
        self.log_config = {'notset': {'maxBytes': 1, 'backupCount': 1},
                           'debug': {'maxBytes': 1, 'backupCount': 1},
                           'info': {'maxBytes': 1, 'backupCount': 1},
                           'warning': {'maxBytes': 1, 'backupCount': 2},
                           'error': {'maxBytes': 5, 'backupCount': 5},
                           'critical': {'maxBytes': 5, 'backupCount': 5}}

        self.init_log_path(log_path)
        self.public_name = 'z' if not name else name
        self.gap = gap

        # initial log container
        self.logs = {}

    def init_log_path(self, log_path=None):

        # get current project path
        def helper():
            root = os.path.dirname(os.path.abspath(__file__))
            if root.find('pack') >= 0:
                root = os.getcwd()
            return root

        #  use current project path by default
        if not log_path:
            log_path = self.log_root = helper()

        # if delivered by "./", use current project path + log_path
        if log_path.startswith('./'):
            self.log_root = helper() + log_path[1:]

        # sometimes we are used to using log or logs
        elif log_path in {'logs', 'log'}:
            self.log_root = helper() + '/' + log_path

        # else log_path maybe an entire path
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
        print('Log path --->>> ', self.log_root)

    def init_config(self, name=None):
        """
        initiaize config of each log level

        :param name:        prefix name of log files

        For example:
            if name = 'web', the log files will look like 'z_web_xxx.log', xxx are names of each level

        Please notice that i've put a "z" if no name passed into Log, for making log files listed at the end of
        all the codes in project.
        """

        logging.Formatter.converter = self.opti_time
        base_format = logging.Formatter('【%(levelname)s】 %(asctime)s [%(process)d] \n%(message)s',
                                        datefmt='%Y-%m-%d %H:%M:%S')

        # logging.Formatter.converter = customTime

        if name not in self.logs:

            # create logger
            logger = logging.getLogger(str(self.log_mapping[name]))
            logger.setLevel(self.log_mapping[name])

            # create handler
            log_path = self.log_root + '/' + self.public_name + '_' + name + '.log'
            base_handler = RotatingFileHandler(log_path, maxBytes=self.log_config[name]['maxBytes'] * 1024 * 1024,
                                               backupCount=self.log_config[name]['backupCount'])

            # define output format
            base_handler.setFormatter(base_format)
            base_handler.setLevel(self.log_mapping[name])

            # add handler
            logger.addHandler(base_handler)

            # critical level add console handler
            if name == 'critical':
                console_handler = logging.StreamHandler()
                console_handler.setLevel(self.log_mapping[name])
                console_format = logging.Formatter('【%(levelname)s】 %(asctime)s [%(process)d] \n%(message)s',
                                                   datefmt='%Y-%m-%d %H:%M:%S')
                console_handler.setFormatter(console_format)
                logger.addHandler(console_handler)
            self.logs.update({name: logger})

    def update_config(self, name: str):
        """
        Add log handler dynamically.
        For avoiding all the log files( including empty log files ) added into log_path during initializing.
        """
        name = name.lower()
        assert name in {'notset', 'debug', 'info', 'warning', 'error', 'critical'}, 'log level is not correct!'
        self.init_config(name)

    @staticmethod
    def combine(*msg, depth=3):
        """
        By this func, you can indirectly receive other three params:
            call_module_name:       point to file which call log function
            call_module_line:       poinrt to line which call log function of "call_module_name"
            call_func_name:         poinrt to func which call log function of "call_module_name"

        In this func, message from log will be combine into the format that builtin func log needs, and for convenience as well.
        Param depth=3 means func can backtrack to 3 calls(raw_func--->>>waring[2]--->>>pre_operate[1]--->>>combine[0]) when reaching combine func.
        As I designed, output format looks like

        2020-01-19 12:59:49,144 WARNING
        ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
        File:     call_module_name
        Func:     call_func_name
        Line:     call_module_line
        Tips:
            tip0:      msg1
            tip1:      msg2
            tip2:      msg3
            ...
        __________________________________________________________________

        """
        call_func_name = sys._getframe(depth).f_code.co_name
        call_module_line = sys._getframe(depth).f_lineno
        call_module_name = sys._getframe(depth).f_code.co_filename

        if str(call_func_name) == '<module>':
            call_func_name = 'NO_FUNC'

        msg = list(msg)
        e = msg[-1]
        if isinstance(e, Exception):
            information = msg[:-1]
            if not information:
                information = ['']
        else:
            e = None
            information = msg
        information = ''.join(['\n    ' + 'tip%s:      %s' % (i + 1, information[i]) for i in range(len(information))])
        if e:
            content = '↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓\n' + \
                      'File:     ' + str(e.__traceback__.tb_frame.f_code.co_filename) + \
                      '\nFunc:     ' + str(e.__traceback__.tb_frame.f_code.co_name) + \
                      '\nLine:     ' + str(e.__traceback__.tb_lineno) + \
                      '\nErrs:     ' + str(e) + \
                      '\nTips:' + \
                      information
        else:
            content = '↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓\n' + \
                      'File:     ' + call_module_name + \
                      '\nFunc:     ' + call_func_name + \
                      '\nLine:     ' + str(call_module_line) + \
                      '\nTips:     ' + \
                      information

        return content + '\n__________________________________________________________________' + '\n'

    def pre_operate(self, *msg, func_name):
        """
        combine messages and udate new logger handler(if new level of log added)
        """
        information = self.combine(*msg, depth=3)
        self.update_config(func_name)
        return information

    def warning(self, *msg):
        func_name = sys._getframe().f_code.co_name
        information = self.pre_operate(*msg, func_name=func_name)
        return self.logs[func_name].warning(information)

    def error(self, *msg):
        func_name = sys._getframe().f_code.co_name
        information = self.pre_operate(*msg, func_name=func_name)
        return self.logs[func_name].error(information)

    def critical(self, *msg):
        func_name = sys._getframe().f_code.co_name
        information = self.pre_operate(*msg, func_name=func_name)
        return self.logs[func_name].critical(information)

    def debug(self, *msg):
        func_name = sys._getframe().f_code.co_name
        information = self.pre_operate(*msg, func_name=func_name)
        return self.logs[func_name].debug(information)

    def notset(self, *msg):
        func_name = sys._getframe().f_code.co_name
        information = self.pre_operate(*msg, func_name=func_name)
        return self.logs[func_name].notset(information)

    def info(self, *msg):
        func_name = sys._getframe().f_code.co_name
        information = self.pre_operate(*msg, func_name=func_name)
        return self.logs[func_name].info(information)

    def opti_time(self, *args):
        utc_tz = timezone('UTC')
        new_datetime = datetime.datetime.now(tz=utc_tz) + datetime.timedelta(hours=self.gap)
        return new_datetime.timetuple()

