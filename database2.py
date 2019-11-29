import pyspark
import py2neo
import pymongo
import elasticsearch as es
import elasticsearch_dsl as esl
from elasticsearch import helpers


class ElasticCon:
    """

    ES的集成模块
    """

    def __init__(self, hosts=['localhost'], port=9200, user=None, password=None, timeout=600):
        self.con_es = es.Elasticsearch(hosts=[{'host': host, 'port': port} for host in hosts], http_auth=(user, password), timeout=timeout)

    def insert(self, data, wrapper=False, _index='tmp', _type='_doc'):
        """

        :param data:         列表, like [{key: value}, ...]
        :param wrapper:      是否需要重组数据
        :param _index:       索引名（类似表名，其实我觉得库名也无所谓- - ）
        :param _type:        类似表说明吧
        :return:
        """
        if wrapper:
            data = ElasticCon.data_wrapper(data, _index, _type)
        helpers.bulk(self.con_es, data)

    @staticmethod
    def data_wrapper(data: list, _index='tmp', _type='_doc', **kwargs):
        """

        :param data:        未打包的list数据
        :param _index:      需要打包的索引_index
        :param _type:       需要打包的类型_type
        :param kwargs:      预留其他可用字段
        :return:
        """
        pre_data = dict({'_index': _index, '_type': _type}, **kwargs)
        data = list(map(lambda x: dict(x, **pre_data), data))
        return data


class SparkCon:
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


class MongoCon:

    def __init__(self):
        self.con_mongo = pymongo.MongoClient(host='', port=0, username='x', password='x', authSource='tmp')

    def z(self):
        db = self.con_mongo['xxx']
        col = db['xxx']
        col.insert_many()
        col.insert_one()


class Neo4jCon:

    def __init__(self):
        self.con_neo4j = py2neo.Graph(host='localhost', auth=('neo4j', '321'))

    def z(self):
        self.con_neo4j.run("""xxxxxx""")

        self.con_neo4j.run("""merge (e: Company{name:'%(name)s'})
        on create
        set e.name='%(name)s'
        """)

        self.con_neo4j.run("""
        match (e:Company{name:'%(node1)s'}), (ee:Company{name:'%(node2)s'})
        merge (e) - [r:%(relation)s] -> (ee)
        return e
        """)
