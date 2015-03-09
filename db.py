#db.py
from pymongo import MongoClient
mClient=MongoClient('54.169.18.100', 27017)
db=mClient.test  #test database
hy=db.hy   #hy collection

l = hy.find_one({'sh600279':{'$exists':True}})
print l['_id'] ,dir(l['_id'].generation_time)

#l['generation_time']= l['_id'].generation_time.now
l.pop('_id', None)



f = open('mongodb_data.json', 'w')
import json
l = json.dumps(l, indent = 4)
l = l.decode("raw_unicode_escape")
l= l.encode("utf8")

f.write(l)
f.close()
