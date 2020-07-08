import pyspark
import py2neo
import elasticsearch as es
from elasticsearch import helpers
import os
import json
import re


class ElasticCon:
    """

    ES的集成模块
    """

    def __init__(self, hosts=['localhost'], port=9200, user=None, password=None, timeout=600):
        self.hosts = hosts
        self.port = port
        self.user = user
        self.password = password
        self.es_con = es.Elasticsearch(hosts=[{'host': host, 'port': port} for host in hosts],
                                       http_auth=(user, password), timeout=timeout)

    def insert(self, data, _index=None, _type='_doc'):
        """

        :param data:         列表, like [{key: value}, ...]
        :param _index:       索引名（类似表名，其实我觉得库名也无所谓- - ）
        :param _type:        类似表说明吧
        :return:

        for example:
                es_con.insert(data=[{'_index': 'ss',
                    '_source':
                        {'name': 'a', 'age': 25}
                     }
                    ])
        or:
                es_con.insert(data=[{'name': 'a', 'age': 25}], _index='ttt')


        """
        if _index:
            data = ElasticCon.data_wrapper(data, _index, _type)
        helpers.bulk(self.es_con, data)

    @staticmethod
    def data_wrapper(data: list, _index, _type='_doc', **kwargs):
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

    def sql2json(self, sql):
        """

        SQL转json的官方接口调用， curl方法
        :param sql:
        :return:
        """
        if self.user and self.password:
            cmd = """curl -XPOST "http://%(user)s:%(password)s@%(host)s:%(port)s/_sql/translate" -H 'Content-Type: application/json' -d'{"query": "%(sql)s"}'""" \
                  % {'host': self.hosts[0],
                     'port': self.port,
                     'user': self.user,
                     'password': self.password,
                     'sql': sql}
        else:
            cmd = """curl -XPOST "http://%(host)s:%(port)s/_sql/translate" -H 'Content-Type: application/json' -d'{"query": "%(sql)s"}'""" \
                  % {'host': self.hosts[0],
                     'port': self.port,
                     'sql': sql}
        f = os.popen(cmd)
        text = f.read()
        f.close()
        return json.loads(text)

    def search(self, query, _index=None, lazy=False):
        """

        search API封装，支持原生sql
        :param query:
        :return:
        """
        if not isinstance(query, dict):
            query = query.lower()
            if not _index:
                _index = re.search('from\s+([^\s]+)\s*?', query).group(1)
            query = self.sql2json(query)
        if not lazy:
            items = self.es_con.search(index=_index, body=query)
            items = items['hits']['hits']
        else:
            items = helpers.scan(self.es_con, index=_index, query=query)
        return items


class SparkCon:
    '''
    examples:

    spark = SparkSQL()
    print(spark.spark.sql("""select * from sharesinfo limit 10""").show())

    '''

    def __init__(self, dbConfig={'host': 'localhost', 'port': 3306, 'user': 'root', 'password': '321', 'dbname': 'main',
                                 'tbname': 'sharesinfo', 'mode': 1}, **kwargs):
        self.dbConfig = dbConfig
        if kwargs:
            self.dbConfig.update(
                {x: kwargs[x] for x in ['host', 'port' 'user', 'password', 'mode', 'dbname', 'tbname'] if x != ''})
        if int(self.dbConfig['mode']) == 1:
            self.dbConfig['driver'] = 'jdbc:mysql'
        self.spark = pyspark.sql.SparkSession.builder.appName('app').config('spark.some.config.option',
                                                                            'some-value').getOrCreate()
        self.spark_con = self.spark.read.jdbc(url="%(driver)s://%(host)s:%(port)s?useSSL=true" % self.dbConfig,
                                              table="%(dbname)s.%(tbname)s" % self.dbConfig,
                                              properties={"user": self.dbConfig['user'],
                                                          "password": self.dbConfig['password']})
        self.spark_con.createOrReplaceTempView(self.dbConfig['tbname'])


class Neo4jCon:

    def __init__(self):
        self.neo4j_con = py2neo.Graph(host='localhost', auth=('neo4j', '321'))

    def z(self):
        self.neo4j_con.run("""xxxxxx""")

        self.neo4j_con.run("""merge (e: Company{name:'%(name)s'})
        on create
        set e.name='%(name)s'
        """)

        self.neo4j_con.run("""
        match (e:Company{name:'%(node1)s'}), (ee:Company{name:'%(node2)s'})
        merge (e) - [r:%(relation)s] -> (ee)
        return e
        """)
