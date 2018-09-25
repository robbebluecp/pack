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
    output = time.strftime("%Y--%m--%d %H:%M:%S", chTime)
    return output
