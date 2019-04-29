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
import copy


class Database:
    """
    该class集成pymssql和pymysql的使用方法，主要做了对insert功能的封装
    其中 1 表示 mysql， 2 表示 sqlserver
    注：2019/04/04 对2表示的pyodbc进行移除，转成pymssl，将来对sqlserver的存储皆使用pymssql，即：2模式

    :param host         :       服务器地址
    :param user         :       用户名
    :param password     :       密码
    :param dbname       :       数据库名
    :param mode         :       连接方式，1表示连接mysql，2表示连接sqlserver

    连接形式如下 :
        dbConfig={'host': 'localhost', 'user': 'root', 'password': 'xxx', 'dbname': 'test', 'mode': 1}
    """

    def __init__(self, host='localhost', port='3306', user='root', password='321', mode=1, dbname='main', tbname='log', charset='utf8', **kwargs):
        self.db_config = copy.deepcopy(locals())
        self.mode = int(mode)
        self.host = host
        self.user = user
        self.passwrod = password
        self.dbname = dbname
        self.tbname = tbname
        self.charset = charset
        self.con = self.get_con(**self.db_config)
        self.cur = self.con.cursor()
        

    @staticmethod
    def get_con(host='localhost', port='3306', user='root', password='321', mode=1, dbname='main', tbname='log', charset='utf8', **kwargs):
        """
        :param host         :       服务器地址
        :param user         :       用户名
        :param password     :       密码
        :param dbname       :       数据库名
        :param mode         :       连接方式，1表示连接mysql，2表示连接sqlserver
        形式如下 :
            dbConfig={'host': 'localhost', 'user': 'root', 'password': 'xxx', 'dbname': 'test', 'mode': 1}
        """

        mode = int(mode)
        host = host
        user = user
        passwrod = password
        dbname = dbname
        tbname = tbname
        charset = charset
        if mode == 1:
            con = pymysql.connect(host='%s' % host, user='%s' % user,
                                  password='%s' % passwrod, charset=charset, database=dbname)

        elif mode == 2:
            con = pymssql.connect(server='%s' % host, user='%s' % user,
                                  password='%s' % passwrod, database='%s' % dbname, charset=charset)
            pymssql.set_max_connections(200000)
        return con

    def build(self,dbname,tbname, data, mode):
        """
           插入方法sql语句封装
           @:param see method "insert"
        """
        field = list(data.keys())


        # sql for mysql, with params of type dict
        if mode == 1:

            data = {key: data[key] if isinstance(data[key], (bytes, )) else str(data[key]) for key in data }
            sql = """insert into %s.%s(%s)values(%s)""" % (
                dbname, tbname, str(field)[1:-1].replace("'", ''),
                '%(' + ('-'.join(field)).replace('-', ')s,%(') + ')s')
            return sql, data

        # sql for pymssql, with params of type tuple
        elif mode == 2:
            value = [str(data[x]) for x in field]
            sql = """insert into %s.dbo.%s(%s)values(%s)""" % (
                dbname, tbname, str(field).replace(", ", '],[').replace("'", ''),
                str('%s,' * len(field))[0:-1])
            return sql, tuple(value)

    @staticmethod
    def tuple_to_dict(data):
        """
        把tuple类型的数据格式转成dict类型
        :param data:    以元组形式存放的list，如：[('name':'罗大黑'), ('age': 25)]
        :return:        以字典形式存放的list，如：{'name': '罗大黑', 'age': 25}
        """
        return dict(data)

    def insert(self,data,dbname=None,tbname=None,mode=None):
        """
        封装插入方法，以字典或列表包含字典或列表包含元组形式.
        :param dbname       :          库名
        :param tbname       :          表明
        :param data         :          数据集，以字典或列表包含字典或列表包含元组形式
                                       字典           {'a': 1, 'b': 2}
                                       列表包含字典    [{'a': 1, 'b': 2}, {'a': 3, 'b': 4}]
                                       列表包含元组    [(a, 1), (b, 2)]
        :param mode         :          mode, different mode leads to different database system
        If mode == 1, the insert sql looks like :
            insert into dbname.tbname (field1, field2, field3) values (%(field1)s, %(field2)s, %(field3)s)
        # if mode == 2:
        #     insert into dbname.tbname (field1, field2, field3) values (?, ?, ?)
        if mode == 3:
            insert into dbname,tbname (field1, field2, field3) values (%s, %s, %s)......
        And your data should be like data={'itemid': xxx, 'itemtitle': xxx}
        """
        if mode is None:
            mode = self.dbConfig['mode']

        if not dbname:
            dbname = self.dbConfig['dbname']
        if not tbname:
            if 'tbname' in self.dbConfig:
                tbname = self.dbConfig['tbname']
            else:
                raise Exception('请在self.dbConfig传入表名或在insert函数传入表名')

        if tbname.find('.') > 0:
            tbname = tbname.split('.')[-1]

        # type dict
        if type(data) == dict:

            result = self.build(dbname,tbname, data, mode)
            self.cur.execute(result[0], result[1])
            self.con.commit()

        # type list with dict or tuple
        if type(data) == list:
            for m_data in data:
                if isinstance(m_data, dict):
                    result = self.build(dbname, tbname, m_data, mode)
                elif isinstance(m_data, list):
                    result = self.tuple_to_dict(m_data)
                self.cur.execute(result[0], result[1])
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
