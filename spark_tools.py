import pyspark


class SparkSQL:
    '''
    examples:

    spark = SparkSQL()
    print(spark.spark.sql("""select * from sharesinfo limit 10""").show())

    '''

    def __init__(self, dbConfig={'host': 'localhost', 'port': 3306, 'user': 'root', 'password': '321', 'dbname': 'main', 'tbname': 'sharesinfo', 'mode': 1}, **kwargs):
        self.dbConfig = dbConfig
        if kwargs:
            self.dbConfig.update({x: kwargs[x] for x in ['host', 'port' 'user', 'password', 'mode', 'dbname', 'tbname'] if x != ''})
        if int(self.dbConfig['mode']) == 1:
            self.dbConfig['driver'] = 'jdbc:mysql'
        self.spark = pyspark.sql.SparkSession.builder.appName('app').config('spark.some.config.option', 'some-value').getOrCreate()
        self.spark_con = self.spark.read.jdbc(url="%(driver)s://%(host)s:%(port)s?useSSL=true" % self.dbConfig,
                                              table="%(dbname)s.%(tbname)s" % self.dbConfig,
                                              properties={"user": self.dbConfig['user'], "password": self.dbConfig['password']})
        self.spark_con.createOrReplaceTempView(self.dbConfig['tbname'])
        

