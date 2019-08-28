try:
    import pymysql
except:
    print('module "pymysql" is not avalable for your recent system circustance')
    pass
try:
    import pymssql
except:
    print('module "pymssql" is not avalable for your recent system circustance')
    pass
import datetime
import os, sys
import elasticsearch


class Database:
    """
    该class集成pymssql和pymysql的使用方法，主要做了对insert功能的封装
    其中 1 表示 mysql， 2 表示 sqlserver

    :param host         :       服务器地址
    :param user         :       用户名
    :param password     :       密码
    :param dbname       :       数据库名
    :param mode         :       连接方式，1表示连接mysql，2表示连接sqlserver

    连接形式如下 :
        db_config={'host': 'localhost', 'user': 'root', 'password': 'xxx', 'dbname': 'test', 'mode': 1}
    """

    def __init__(self, host='localhost', port=3306, user='root', password='321', mode=1, dbname='main', tbname='log',
                 charset='utf8', dbConfig=None, **kwargs):
        if dbConfig:
            self.mode = int(dbConfig['mode']) if dbConfig.get('mode') else mode
            self.host = dbConfig['host'] if dbConfig.get('host') else host
            if self.mode == 2:
                self.port = 1433
            else:
                self.port = 3306
            self.user = dbConfig['user'] if dbConfig.get('user') else user
            self.password = dbConfig['password'] if dbConfig.get('password') else password
            self.dbname = dbConfig['dbname'] if dbConfig.get('dbname') else dbname
            self.tbname = dbConfig['tbname'] if dbConfig.get('tbname') else tbname
            self.charset = dbConfig['charset'] if dbConfig.get('charset') else charset
        else:
            self.mode = int(mode)
            self.host = host
            self.port = port
            if self.mode == 2:
                self.port = 1433
            self.user = user
            self.password = password
            self.dbname = dbname
            self.tbname = tbname
            self.charset = charset
        self.con = self.get_con(host=self.host, port=self.port, user=self.user, password=self.password, mode=self.mode,
                                dbname=self.dbname, tbname=self.tbname, charset=self.charset)
        self.cur = self.con.cursor()

    @staticmethod
    def get_con(host='localhost', port=3306, user='root', password='321', mode=1, dbname='main', tbname='log',
                charset='utf8', **kwargs):
        """
        :param host         :       服务器地址
        :param user         :       用户名
        :param password     :       密码
        :param dbname       :       数据库名
        :param mode         :       连接方式，1表示连接mysql，2表示连接sqlserver
        形式如下 :
            db_config={'host': 'localhost', 'user': 'root', 'password': 'xxx', 'dbname': 'test', 'mode': 1}
        """

        if mode == 1:
            con = pymysql.connect(host='%s' % host, user='%s' % user, port=int(port),
                                  password='%s' % password, charset=charset, database=dbname)

        elif mode == 2:
            con = pymssql.connect(server='%s' % host, user='%s' % user, port='%s' % port,
                                  password='%s' % password, database='%s' % dbname, charset=charset)
            pymssql.set_max_connections(200000)
        return con

    def build(self, dbname, tbname, data, mode):
        """
           插入方法sql语句封装
           @:param see method "insert"

           data: [(field1, field2, field3, ....), [(data1, data2, data3,...), (data1, data2, data3,...), ......]]
        """
        if isinstance(data, dict):
            field = tuple(data.keys())
            values = [tuple(data[x] for x in field)]
        elif isinstance(data, list) and isinstance(data[0], dict):
            field = tuple(data[0].keys())
            values = [tuple(sub_data[x] for x in sub_data) for sub_data in data]
        else:
            field = data[0]
            if not isinstance(field, tuple):
                field = tuple(field)
            values = data[1]

        if mode == 1:

            sql = """insert into %s.%s %s values ({})""" % (
                dbname,
                tbname,
                str(field).replace("'", '`')
            )
            sql = sql.format(('%s,' * len(field))[:-1])
            return sql, values

        elif mode == 2:
            sql = """insert into %s.dbo.%s %s values ({})""" % (
                dbname,
                tbname,
                str(field).replace("'", '')
            )
            sql = sql.format(('%s,' * len(field))[:-1])
            return sql, values

    def insert(self, data, dbname=None, tbname=None, mode=None, size=10000):
        """

        2019-08-05 全部改用insertmany方法，速度提升约五倍

        封装插入方法，以字典或列表包含字典或列表包含元组形式.
        :param dbname       :          库名
        :param tbname       :          表明
        :param data         :          数据集，为如下形式

                                       data = [(field1, field2, field3, ......),
                                               [(data1, data2, data3, ...), (data1, data2, data3, ...), (data1, data2, data3, ...)]

        :param mode         :          mode, different mode leads to different database system

        insert into dbname.tbname (field1, field2, field3) values (%s, %s, %s)

        """
        if mode is None:
            mode = self.mode

        if not dbname:
            dbname = self.dbname

        if not tbname:
            tbname = self.tbname

        if tbname.find('.') > 0:
            tbname = tbname.split('.')[-1]

        # type list with dict or tuple
        result = self.build(dbname, tbname, data, mode)
        columns, values = result
        for i in range(len(values) // size + 1):
            self.cur.executemany(columns, values[i*size: (i+1)* size])
            self.con.commit()

    def execute(self, sql, *params):
        self.cur.execute(sql, *params)
        return self.cur

    def commit(self):
        self.con.commit()

    def fetchall(self):
        self.cur.fetchall()

    def fetchone(self):
        self.cur.fetchone()

    def close(self):
        self.con.close()


class ES:
    def __init__(self,
                 host:str='localhost',
                 port: int=9200):
        self.client = elasticsearch.Elasticsearch(hosts=[{"host": host, "port": port}])

    def search(self,
               index:str='bank',
               body:dict={"size": "1000"}):


        response = self.client.search(index=index, body=body)
        items = response['hits']['hits']
        return items

    def insert(self,
               index:str,
               data:list):
        data = [{"_index": index, "_type": "_doc", "_source": i} for i in data]
        elasticsearch.helpers.bulk(self.client, data)
