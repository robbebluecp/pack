import socket
import time
import datetime
from hashlib import md5, sha1
import emoji
from googletrans import Translator
from typing import List, Dict


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
def date_to_char(type='s', ctime=None):
    """
    当前时间转成年月日时分秒形式
    :return:
    """
    if not ctime:
        ctime = datetime.datetime.now()
    if type == 's':
        return ctime.strftime('%Y%m%d%H%M%S')
    elif type == 'm':
        return ctime.strftime('%Y%m%d%H%M')


def emoji_transfer(chars: str or List[str]) -> str or List[str]:
    """
    对字符的表情进行转换
    :param char:
    :return:
    """
    result = []
    if isinstance(chars, list):
        for char in chars:
            result.append(emoji.demojize(char))
        return result
    else:
        return emoji.demojize(chars)


def translate_to_en(chars: str or List[str] or iter,
                    dest: str = 'en',
                    translator: Translator = None,
                    return_type: str = 'list') -> List[str]:
    """
    谷歌翻译
    :param chars:
    :param dest:        zh-cn
    :param translator:
    :param return_type:
    :return:
    """
    if isinstance(chars, str):
        chars = [chars]
    if not translator:
        translator = Translator(service_urls=['translate.google.cn'])
    result = translator.translate(chars, dest=dest)
    if return_type == 'list':
        return list(map(lambda x: x.text, result))
    else:
        return result


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
