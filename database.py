import pymysql
import pymongo
import rejson
import oss2


def check_sock(func):
    """

    重置连接装饰器, 连接池的底层实现逻辑
    :param func:
    :return:
    """

    def wrapper(self, *args, **kwargs):
        if not self.ping():
            self.reconnect()
        return func(self, *args, **kwargs)

    return wrapper


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

    def __init__(self, host='localhost', port=3306, user='root', password='321', mode=1, dbname='mysql', tbname='db',
                 charset='utf8', db_config=None, **kwargs):
        if db_config:
            self.mode = int(db_config['mode']) if db_config.get('mode') else mode
            self.host = db_config['host'] if db_config.get('host') else host
            if self.mode == 2:
                self.port = 1433
            else:
                self.port = 3306
            self.user = db_config['user'] if db_config.get('user') else user
            self.password = db_config['password'] if db_config.get('password') else password
            self.dbname = db_config['dbname'] if db_config.get('dbname') else dbname
            self.tbname = db_config['tbname'] if db_config.get('tbname') else tbname
            self.charset = db_config['charset'] if db_config.get('charset') else charset
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
        self.db_config = {'mode': self.mode, 'host': self.host, 'port': self.port, 'user': user, 'password': password if password else '',
                         'dbname': dbname, 'tbname': tbname}
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
        else:
            assert 1 == 0, 'mode is must be 1 !'
        # sqlserver
        # elif mode == 2:
        #     con = pymssql.connect(server='%s' % host, user='%s' % user, port='%s' % port,
        #                           password='%s' % password, database='%s' % dbname, charset=charset)
        #     pymssql.set_max_connections(200000)
        return con

    def build(self, dbname, tbname, data, mode):
        """
           插入方法sql语句封装
           @:param see method "insert"

           data: [(field1, field2, field3, ....), [(data1, data2, data3,...), (data1, data2, data3,...), ......]]
        """
        if isinstance(data, dict):
            assert 1 == 0, '不允许是字典！！！'
        if isinstance(data, list) and isinstance(data[0], dict):
            field = tuple(data[0].keys())
            values = [tuple(sub_data[x] for x in sub_data) for sub_data in data]
        else:
            field = data[0]
            if not isinstance(field, tuple):
                field = tuple(field)
            values = data[1]

        if mode == 1:

            field_char = str(field).replace("'", '`')
            if len(field) == 1:
                field_char = field_char.replace(',', '')
            sql = """insert into `%s`.`%s` %s values ({})""" % (
                dbname,
                tbname,
                field_char
            )
            sql = sql.format(('%s,' * len(field))[:-1])

            return sql, values

        # sqlserver
        # elif mode == 2:
        #     sql = """insert into %s.dbo.%s %s values ({})""" % (
        #         dbname,
        #         tbname,
        #         str(field).replace("'", '')
        #     )
        #     sql = sql.format(('%s,' * len(field))[:-1])
        #     return sql, values

    @check_sock
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
            self.cur.executemany(columns, values[i * size: (i + 1) * size])
            self.con.commit()

    @check_sock
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

    def ping(self):
        return True if self.con._sock else False

    def reconnect(self):
        self.con = self.get_con(**self.db_config)
        self.cur = self.con.cursor()


class RedisCon(rejson.Client):
    def __init__(self, host='localhost', port=6379, password='', db=0, *args, **kwargs):
        self.params = dict({'host': host, 'port': port, 'password': password, 'db': db, 'decode_responses': True},
                           **kwargs)
        super(RedisCon, self).__init__(**self.params)

    def change_db(self, db=0):
        self.params['db'] = db
        self.execute_command("""select %s""" % db)
        self.params['db'] = int(db)

    def select(self, db=0):
        return self.change_db(db)

    def __repr__(self):
        return "%s<%s>" % (
            type(self).__name__, self.params
        )


class MongoCon:

    def __init__(self, host='localhost', port=27017, user='root', password='321', auth_db='admin', dbname='tmp', colname='tmp',
                 charset='utf8', db_config=None, use_uri=False, uri=None, **kwargs):
        self.auth_db = auth_db
        self.colname = colname
        self.dbname = dbname
        if isinstance(port, str):
            port = int(port)

        if uri:
            self.mongo_con = pymongo.MongoClient(uri)
        elif use_uri and not uri:
            self.mongo_con = pymongo.MongoClient(
                'mongodb://%(user)s:%(password)s@%(host)s:%(port)s/?authSource=%(dbname)s' % {'user': user,
                                                                                              'password': password,
                                                                                              'host': host,
                                                                                              'port': port,
                                                                                              'dbname': auth_db})
        else:
            self.mongo_con = pymongo.MongoClient(host=host, port=port, username=user, password=password,
                                                 authSource=auth_db)

    def db(self, dbname=None):
        dbname = dbname or self.dbname or 'tmp'
        return self.mongo_con[dbname]

    def col(self, colname=None, dbname=None):
        dbname = dbname or self.dbname or 'tmp'
        colname = colname or self.colname
        return self.db(dbname)[colname]


MysqlCon = Database


class OssCon:
    def __init__(self, AccessKeyId, AccessKeySecret, BucketRegion=None, BucketName=None):
        """
        params:
            AccessKeyId:        oss AccessKeyId
            AccessKeySecret:    oss AccessKeySecret
            BucketRegion:       a url like:http://oss-cn-hongkong-internal.aliyuncs.com,
                                hongkong means region of your bucket, if not use internal
                                internet, remove "-internal"
            BucketName:         your bucket name
        """
        self.auth = oss2.Auth(AccessKeyId, AccessKeySecret)
        self.AccessKeyId, self.AccessKeySecret = AccessKeyId, AccessKeySecret
        self.BucketRegion = BucketRegion
        self.BucketName = BucketName
        if BucketRegion and BucketName:
            self.bucket = oss2.Bucket(self.auth, BucketRegion, BucketName)

    def get_bucket(self, BucketRegion: str = None, BucketName: str = None):
        """
        function to set bucket whenever you want if BucketRegion and BucketName not set when initializing
        """
        BucketRegion = BucketRegion or self.BucketRegion
        BucketName = BucketName or self.BucketName
        self.bucket = oss2.Bucket(self.auth, BucketRegion, BucketName)

    def push_bytes(self, name, data):
        """
        params:
            name:       file name in oss bucket
            data:       bytes data of anything, like images, mp4 and so on
        """
        self.bucket.put_object(name, data)

    def push_file(self, name, file_name):
        """

        upload your local file(file_name) to oss with a new "name"
        """
        self.bucket.put_object_from_file(name, file_name)

