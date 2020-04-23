import socket
import time
import datetime
from hashlib import md5, sha1


def get_local_ip():
    """
    获取本地内网ip
    """
    ip = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
    except:
        pass
    return ip


def encrypt(char, method='md5'):
    """
    支持md5和sha1加密方式
    :param char:
    :param method:
    :return:
    """
    char = str(char)
    if method == 'md5':
        m = md5()
    elif method == 'sha1':
        m = sha1()
    m.update(char.encode('utf8'))
    return m.hexdigest()


def stamp_to_date(time_int: int or str):
    '''
    时间戳转GTM+8（东八区）时间,
    :param time_int:
    :param time_int(int):       十位数时间戳
    :return(datatime):          时间

    examples:
            print(time_stamp(1547111111))
    '''
    ll = len(str(time_int))
    if isinstance(time_int, str):
        time_int = int(time_int[:10])
    if ll > 10:
        time_int = int(time_int / 10 ** (ll - 10))

    chTime = time.localtime(time_int)
    output = time.strftime("%Y-%m-%d %H:%M:%S", chTime)
    return output


# 当前时间转固定格式
def date_to_char(type='s'):
    """
    当前时间转成年月日时分秒形式
    :return:
    """
    if type == 's':
        return datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    elif type == 'm':
        return datetime.datetime.now().strftime('%Y%m%d%H%M')


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
