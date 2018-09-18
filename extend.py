import ctypes


def kill(tid, theType=SystemExit):
    try:
        id = ctypes.c_long(tid.ident)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(id, ctypes.py_object(theType))
        if res == 0:
            print('Invaild thread id !')
    except Exception as e:
        print('Fail to kill thread, Error is : ' + str(e))

