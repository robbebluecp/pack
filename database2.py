import pymongo
import py2neo


con_mongo = pymongo.MongoClient()
con = pymongo.MongoClient(host='', port=0, username='x', password='x', authSource='tmp')
db = con['xxx']
col = db['xxx']
col.insert_many()
col.insert_one()


con_neo4f = py2neo.Graph(host='localhost', auth=('neo4j', '321'))
con_neo4f.run("""xxxxxx""")

con.run("""merge (e: Company{name:'%(name)s'})
on create
set e.name='%(name)s'
""" )

con.run("""
match (e:Company{name:'%(node1)s'}), (ee:Company{name:'%(node2)s'})
merge (e) - [r:%(relation)s] -> (ee)
return e
""" )