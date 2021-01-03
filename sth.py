import platform
import random
import time

plf = platform.platform().lower()

if plf.startswith('darwin'):
    from .sth_mac import *
elif plf.startswith('linux'):
    from .sth_linux import *
else:
    assert ImportError ,'暂不支持非linux、mac平台'