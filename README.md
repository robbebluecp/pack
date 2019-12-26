
# Amazing Pack For Human Beings 。。。 Hahaha ！

## Summary

### 高频
- __[crawl.py](https://github.com/yfyvan/pack/blob/master/crawl.py)__   
请求模块，主要用于请求url，包括data的json或str类型的post请求，同时也支持返回二进制数据流

- __[database.py](https://github.com/yfyvan/pack/blob/master/database.py)__   
数据库连接模块，集成pymysql和pymssql的连接方式，支持列表和字典数据插入方式。

- __[log.py](https://github.com/yfyvan/pack/blob/master/log.py)__   
日志模块。可以分开记录三个等级（warning、error和critical）的日志，支持多进程锁

- __[extend.py](https://github.com/yfyvan/pack/blob/master/extend.py)__   
存放了一些自己编写的常用功能函数，包括字体颜色、时间戳转换等


### 低频
- __[nlp.py](https://github.com/yfyvan/pack/blob/master/nlp.py)__  
nlp常用模块，当前制作了"词向量"类和"聚类"两个类，后续会慢慢添加常用类

- __[cvs.py](https://github.com/yfyvan/pack/blob/master/cvs.py)__  
图像增强模块，用于深度学习图像分类的图像增强

- __[parseconfig.py](https://github.com/yfyvan/pack/blob/master/parseconfig.py)__  
继承重写Parseconfig类，支持大小写敏感、字典、int类型 

- __[useragent.py](https://github.com/yfyvan/pack/blob/master/useragent.py)__   
收集的一些请求头信息

- __[spark_tools.py](https://github.com/yfyvan/pack/blob/master/spark_tools.py)__  
用于python对接spark的入口，已可用，待完善

## Installation

- **(1)pip3 install git+https://github.com/yfyvan/pack.git (Recomanded)**  
因为这是最新的，一般我会先push到github而不是到pypi

- **(2)pip3 install lpack**

