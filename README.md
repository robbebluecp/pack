
## 包说明

- __[crawl.py](https://github.com/ldhsight/pack/blob/master/crawl.py)__ 请求模块，主要用于请求url，包括data的json或str类型的post请求。

- __[database.py](https://github.com/ldhsight/pack/blob/master/database.py)__ 数据库连接模块，集成pyodbc、pymsql和pymssql的连接方式，支持列表和字典数据插入方式。

- __[log.py](https://github.com/ldhsight/pack/blob/master/log.py)__ 日志模块。可以分开记录三个等级（warning、error和critical）的日志，支持多进程锁

- __[useragent.py](https://github.com/ldhsight/pack/blob/master/useragent.py)__ 收集的一些请求头信息

- __[mitmbooks.py](https://github.com/ldhsight/pack/blob/master/mitmbooks.py)__ 中间人攻击模块，支持各种http、https协议相关信息抽取

- __[extend.py](https://github.com/ldhsight/pack/blob/master/extend.py)__ 存放了一些自己编写的常用功能函数，包括字体颜色、时间戳转换等

- __[parseconfig.py](https://github.com/ldhsight/pack/blob/master/parseconfig.py)__ 继承重写Parseconfig类，支持大小写敏感和字典和int类型

