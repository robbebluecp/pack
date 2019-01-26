import ctypes
import time

def kill(tid, theType=SystemExit):
    '''
    杀线程的方法，不安全，不建议用
    :param tid(object):     进程变量名
    :param theType:
    :return:

    examples:
            thread_1 = threading.Thread(xxxxxxxxxx)
            thread_1.start()
            ......
            kill(thread_1)
    '''
    try:
        id = ctypes.c_long(tid.ident)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(id, ctypes.py_object(theType))
        if res == 0:
            print('Invaild thread id !')
    except Exception as e:
        print('Fail to kill thread, Error is : ' + str(e))

def softmax(x_input):
    x_input = np.asarray(x_input, dtype=np.float) / max(x_input)
    return np.exp(x_input) / np.sum(np.exp(x_input))


def sigmoid(x_input):
    return 1.0 / (1.0 + np.exp(-(np.asarray(x_input, dtype=np.float))))

def time_stamp(time_int):
    '''
    时间戳转GTM+8（东八区）时间,
    :param time_int(int):       十位数时间戳
    :return(datatime):          时间

    examples:
            print(time_stamp(1547111111))
    '''
    chTime = time.localtime(time_int)
    output = time.strftime("%Y-%m-%d %H:%M:%S", chTime)
    return output


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

    if len(char) > len(c):
        print('字符长度和颜色长度不一致, 返回原始字体')
        print(*char)
        return

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