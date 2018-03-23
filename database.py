try:
    import pyodbc
except:
    print('module "pyodbc" is not avalable for your recent system circustance')
    pass
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


class Database:
    """
    This class support three ways to connect to database system.
    At first you have to get one of these packages : pymysql, pyodbc, pymssql.
    Param dbConfig is a dictionary including at least the following params : host, user, password, dbname.

    :param host         :       the server name or ip of your database system
    :param user         :       user's login name or id ect
    :param password     :       your password
    :param dbname       :       database name that you want to use
    :param mode         :       the way you choose to use to connect to database system
                                1 means pymysql to mysql, 2 means pyodbc to sqlserver and 3 is pymssql to sqlserver

    So the dbConfig should looks like :

        dbConfig = {'host': 'localhost', 'user': 'root', 'password': 'xxx', 'dbname': 'test', 'mode': 1}

    """

    def __init__(self, dbConfig):
        self.dbconfig = dbConfig
        self.dbconfig['mode'] == int(self.dbconfig['mode'])

        if self.dbconfig['mode'] == 1:
            self.con = pymysql.connect(host='%s' % self.dbconfig['host'], user='%s' % self.dbconfig['user'],
                                       password='%s' % self.dbconfig['password'], charset="utf8")

        elif self.dbconfig['mode'] == 2:
            self.con = pyodbc.connect(
                'DRIVER={SQL Server};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s' % (
                self.dbconfig['host'], self.dbconfig['dbname'], self.dbconfig['user'], self.dbconfig['password']))

        else:
            self.con = pymssql.connect(server='%s'% self.dbconfig['host'], user='%s' % self.dbconfig['user'],
                                        password='%s' % self.dbconfig['password'], database='%s' % self.dbconfig['dbname'])

        self.cur = self.con.cursor()

    @staticmethod
    def build(mode, data):

        # field = list(sorted(data.keys(), key=lambda x: x[0]))
        field = list(data.keys())
        value = [str(data[x]) for x in field]

        # sql for mysql, with params of type dict
        if mode == 1:
            sql = """insert into %s.%s(%s)values(%s)""" % (
                dbname, tbname, str(field)[1:-1].replace("'", ''),
                '%(' + ('-'.join(field)).replace('-', ')s,%(') + ')s')

        # sql for pyodbc, with params of type list
        elif mode == 2:
            sql = """insert into %s.dbo.%s (%s) values (%s)""" % (
                dbname, tbname, str(field)[1:-1].replace("'", ''),
                (len(field) * '?,')[:-1])
        # sql for pymssql, with params of type tuple
        else:
            sql = """insert into %s.dbo.%s(%s)values(%s)""" % (
                dbname, tbname, str(field)[1:-1].replace("'", ''),
                str('%s,' * len(field))[0:-1])

        return sql

    def insert(self,dbname,tbname,data,mode=2):
        """
        This methed support some convenient ways for you to insert your data into database.

        :param dbname       :          name of database
        :param tbname       :          name of table
        :param data         :          data you that want to insert into, type dict
        :param mode         :          mode, different mode leads to different database system

        If mode == 1, the insert sql looks like :
            insert into dbname.tbname (field1, field2, field3) values (%(field1)s, %(field2)s, %(field3)s)

        if mode == 2:
            insert into dbname.tbname (field1, field2, field3) values (?, ?, ?)

        if mode == 3:
            insert into dbname,tbname (field1, field2, field3) values (%s, %s, %s)......

        And your data should be like data={'itemid': xxx, 'itemtitle': xxx}

        """

        if type(data) == dict:
            sql = build(mode, data)
            self.cur.execute(sql, data)
            self.cur.commit()

        if type(data) == list:
            for m_data in data:
                sql = build(mode, data)
                self.cur.execute(sql, data)
                self.cur.commit()

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
        self.cur.close()
