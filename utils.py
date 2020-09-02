import socket
import time
import datetime
from hashlib import md5, sha1
import emoji
from googletrans import Translator
from typing import List, Dict
import urllib.parse
from . import crawl
import json
import re


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


# 定时器
def control(star_time: int or float = 0,
            cycle: int or float = 86400,
            scope: int or float = 100):
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


def google_trans(chars: str or List[str] or iter,
                    translator: Translator = None,
                    return_type: str = 'list',
                    dest='en',
                    service_urls=['translate.google.cn']) -> List[str]:
    """
    谷歌翻译
    :param chars:
    :param translator:
    :param return_type:
    :return:
    """
    if isinstance(chars, str):
        chars = [chars]
    if not translator:
        translator = Translator(service_urls=service_urls)
    result = translator.translate(chars, dest=dest)
    if return_type == 'list':
        return list(map(lambda x: x.text, result))
    else:
        return result

def baidu_trans(app_id: str,
                secret_key: str,
                query: str,
                from_lan: str = 'auto',
                to_lan: str = 'en',
                salt='robbe'
                ):
    """

    :param app_id:              your baidu api app_id
    :param secret_key:          your baidu api secret_key
    :param query:               something need to translate
    :param from_lan:            from 【xxx】 language
    :param to_lan:              to 【xxx】 language
    :param salt:                salt
    :return:
    """

    sign = app_id + query + str(salt) + secret_key
    sign = md5(sign.encode()).hexdigest()
    nn = 0
    while nn < 10:
        try:
            sub_url = '/api/trans/vip/translate' + '?appid=' + app_id + '&q=' + urllib.parse.quote(
                query) + '&from=' + from_lan + '&to=' + to_lan + '&salt=' + str(
                salt) + '&sign=' + sign

            url = 'https://fanyi-api.baidu.com/api/trans/vip/translate' + sub_url
            html = crawl.crawl(url).html
            data = json.loads(html)
            des_sentence = data['trans_result'][0]['dst']
            return des_sentence
        except Exception as e:
            print(e)
            nn += 1
    return None


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


def bytes_to_str(bytes_array):
    result = ''
    i = 0
    while i < len(bytes_array):
        value = bytes_array[i]
        if value >= 0:
            char = chr(value)
            i += 1
        else:
            tmp = ''
            values = bytes_array[i:i + 3]
            for value in values:
                value = 256 + value
                tmp += str(hex(value)).replace('0x', '\\x')
            i += 3
            char = eval(repr(tmp.encode('utf8')).replace('\\\\', '\\'))
            char = char.decode('utf8')
        result += char
    return result


def string_to_bytes(string):
    result = []
    for i in string:
        num = ord(i)
        if num < 256:
            result.append(num)
        if num > 255:
            values = bytes(i, encoding='utf8')
            values = re.findall('\\\\x[a-zA-Z0-9]{2}', str(values))
            values = list(map(lambda x: x.replace('\\', '0'), values))
            for value in values:
                result.append(- (256 - int(value, base=16)))
    return result