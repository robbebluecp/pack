try:
    import pyodbc
except:
    print('package or module "pyodbc" is not avalable for your recent system circustance')
    pass
try:
    import pymysql
except:
    pass
try:
    import pymssql
except:
    pass


class Database:
    """
    This class support three ways to connect to database system.
    At first you have to get one of these packages : pymysql, pyodbc, pymssql.
    Param dbConfig is a dictionary including at lest the following params : host, user, password, dbname.

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

        if int(self.dbconfig['mode']) == 1:
            self.con = pymysql.connect(host='%s' % self.dbconfig['host'], user='%s' % self.dbconfig['user'],
                                       password='%s' % self.dbconfig['password'], charset="utf8")

        elif int(self.dbconfig['mode']) == 2:
            self.con = pyodbc.connect(
                'DRIVER={SQL Server};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s' % (
                self.dbconfig['host'], self.dbconfig['dbname'], self.dbconfig['user'], self.dbconfig['password']))

        else:
            self.con = pymssql.connect(server='%s'% self.dbconfig['host'], user='%s' % self.dbconfig['user'],
                                        password='%s' % self.dbconfig['password'], database='%s' % self.dbconfig['dbname'])

        self.cur = self.con.cursor()

    def insert(self,dbname,tbname,data,mode=2):
        """
        This methed support some convenient ways for you to insert your data into database.

        :param dbname       :          name of database
        :param tbname       :          name of table
        :param data         :          data you that want to insert into, it should be a dictionay
        :param mode         :          mode, diferent mode leads to diferent database system

        If mode == 1, the insert sql looks like :
            insert into dbname.tbname (field1, field2, field3) values (%(field1)s, %(field2)s, %(field3)s)

        if mode == 2:
            insert into dbname.tbname (field1, field2, field3) values (?, ?, ?)

        if mode == 3:
            insert into dbname,tbname (field1, field2, field3) values (%s, %s, %s)......

        And your data should be like data={'itemid': xxx, 'itemtitle': xxx}

        """
        field = list(sorted(data.keys(),key=lambda x:x[0]))
        value = [str(data[x]) for x in field]
        mode = int(mode)

        if mode == 1:
            sql = """insert into %s.%s(%s)values(%s)""" % (
                dbname, tbname, str(field)[1:-1].replace("'", ''),
                '%(' + ('-'.join(field)).replace('-', ')s,%(') + ')s')
            self.cur.execute(sql, data)
            self.cur.commit()

        elif mode == 2:
            sql = """insert into %s.dbo.%s (%s) values (%s)""" % (
                dbname, tbname, str(field)[1:-1].replace("'", ''),
                (len(field) * '?,')[:-1])
            self.cur.execute(sql, value)
            self.cur.commit()

        else:
            print(mode)
            sql = """insert into %s.dbo.%s(%s)values(%s)""" % (
            dbname, tbname, str(field)[1:-1].replace("'", ''),
            str('%s,' * len(field))[0:-1])
            print(sql)
            self.cur.execute(sql, tuple(value))
            self.con.commit()

    def execute(self, sql, *params):
        if int(self.dbconfig['mode']) == 1:
            self.cur.execute(sql, *params)
        else:
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
