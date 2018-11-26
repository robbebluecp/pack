import ctypes
import time

def kill(tid, theType=SystemExit):
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
    chTime = time.localtime(time_int)
    output = time.strftime("%Y-%m-%d %H:%M:%S", chTime)
    return output


def cprint(*char, c=None):
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