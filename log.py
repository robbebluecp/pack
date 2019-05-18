import logging
from concurrent_log_handler import ConcurrentRotatingFileHandler as RotatingFileHandler
import os
import sys
import platform

"""
NOTSET   0
DEBUG    10
INFO    20
WARNING   30
ERROR    40
CRITICAL  50

examples:
    (1) log.warning('This is A warning message')

    (1) log.critical('This is A critical message')
"""
# 路径提取操作在程序链式启动时会出现问题，使用如下方法进行fix
# path = (os.path.dirname(sys.argv[0]) + '/').replace('//', r'/')
# if platform.platform().lower().find('linux') >= 0:
#   path = os.getcwd() + '/'

path = os.path.dirname(os.path.abspath(__file__)) + '/'
if path.find('pack') >= 0:
    path = os.getcwd() + '/'

warningFilter = logging.Filter()
errorFilter = logging.Filter()
criticalFilter = logging.Filter()

# 区分日志等级
warningFilter.filter = lambda level: 30 <= level.levelno <= 30
errorFilter.filter = lambda level: 40 <= level.levelno <= 40
criticalFilter.filter = lambda level: 50 <= level.levelno <= 50

# 日志分三个等级
warningOperation = RotatingFileHandler(path + 'z_warning.log', maxBytes=1 * 1024 * 1024, backupCount=1)
warningOperation.addFilter(warningFilter)
warningFormat = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
warningOperation.setFormatter(warningFormat)

errorOperation = RotatingFileHandler(path + 'z_error.log', maxBytes=10 * 1024 * 1024, backupCount=5)
errorOperation.addFilter(errorFilter)
errorFormat = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
errorOperation.setFormatter(errorFormat)

criticalOperation = RotatingFileHandler(path + 'z_critical.log', maxBytes=10 * 1024 * 1024, backupCount=2)
criticalOperation.addFilter(criticalFilter)
criticalFormat = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
criticalOperation.setFormatter(criticalFormat)


console = logging.StreamHandler()
console.setLevel(50)
consoleFormat = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
console.setFormatter(consoleFormat)

log = logging.getLogger()
log.setLevel(logging.DEBUG)
log.addHandler(warningOperation)
log.addHandler(errorOperation)
log.addHandler(criticalOperation)
log.addHandler(console)


def conbine(msg, e):
  content = 'File:' + str(e.__traceback__.tb_frame.f_code.co_filename) + '------Line:' + str(e.__traceback__.tb_lineno) + '------Error:' + str(e) + '------Tips:' + str(msg)
  return content

def debug(msg, e=None, *args, **kwargs):
  if e:
    msg = conbine(msg, e)
  return log.debug(msg, *args, **kwargs)
def info(msg, e=None, *args, **kwargs):
  if e:
    msg = conbine(msg, e)
  return log.info(msg, *args, **kwargs)
def warning(msg, e=None, *args, **kwargs):
  if e:
    msg = conbine(msg, e)
  return log.warning(msg, *args, **kwargs)
def error(msg, e=None, *args, **kwargs):
  if e:
    msg = conbine(msg, e)
  return log.error(msg, *args, **kwargs)
def critical(msg, e=None, *args, **kwargs):
  if e:
    msg = conbine(msg, e)
  return log.critical(msg, *args, **kwargs)

