import ctypes
import time
import datetime
import numpy as np
from hashlib import md5


def get_md5(char):
    m = md5()
    m.update(char.encode('utf8'))
    return m.hexdigest()


def time_stamp(time_int):
    '''
    时间戳转GTM+8（东八区）时间,
    :param time_int(int):       十位数时间戳
    :return(datatime):          时间

    examples:
            print(time_stamp(1547111111))
    '''
    if isinstance(time_int, str):
        time_int = int(time_int[:10])
    chTime = time.localtime(time_int)
    output = time.strftime("%Y-%m-%d %H:%M:%S", chTime)
    return output

# 当前时间转固定格式
def time_to_char():
    return datetime.datetime.now().strftime('%Y%m%d%H%M%S')

# 定时器
def control(star_time: int, cycle: int = 86400, scope: int = 100):
    """

    :param star_time:       任务开始时间
    :param cycle:           任务周期
    :param scope:           开始时间波动范围
    :return:
    """
    if scope + star_time * 3600 <= (int(time.time()) + 8 * 3600) % cycle <= scope * 2 + star_time * 3600:
        return 1
    else:
        return 0

# pycharm专用，颜色字体打印
def cprint(*char, c=None):
    '''
    打印有颜色字体
    :param char(str or *str):       需要print的字符，可print多组字符
    :param c(list or str):          如果为str，则所有字体都是一个颜色；如果为list，长度需=字符组长度
    :return:

    examples:
            cprint('aaa', 'bbb','ccc', c=['r', 'g', 'b'])
    '''
    dic = {'r': '91',
           'g': '92',
           'y': '93',
           'b': '94',
           'p': '95',
           'q': '96',
           'z': '107,'
           }
    if c is None:
        print(*char)
        return

    if len(char) > len(c) and isinstance(c, list):
        c = c[0]

    try:
        if type(c) == str and c in dic:
            print(*(map(lambda x: '\033[' + dic[c] + 'm' + str(x) + '\033[0m', char)))
            return
        if type(c) == list:
            if len(c) != len(char):
                print(*(map(lambda x: '\033[' + dic['z'] + 'm' + str(x) + '\033[0m', char)))
                return
            else:
                print(*(map(lambda x, y: '\033[' + dic[y] + 'm' + str(x) + '\033[0m', char, c)))
                return
    except Exception as e:
        print(*char)
        return