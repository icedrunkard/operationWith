# -*- coding: utf8 -*-
import pymongo
import redis
#from .settings import COLLECTION_NAME,MONGO_DATABASE,MONGO_HOST
#from .settings import MONGO_HOST
client = pymongo.MongoClient('localhost:27009')
#db = client[MONGO_DATABASE]#变更学校
#col=db[COLLECTION_NAME+'_papers']#变更学院
SCHOOL_LIST=['THU','ZJU','FUDAN','BIT','BNU','BUAA','TONGJI',]


db2=client['schools']
col2=db2['dpts_985']

def GetPaperAuthors(short,dpt):
    db=client[short]
    col=db[dpt+'_papers1']
    s=set()
    for i in col.find():
        for a in i['author']:
            s.add(a['name'])
    return s




def NameToRedis():#变更host
    db=redis.StrictRedis(host='localhost',#host='localhost'host='123.206.177.39'
                         port='6379',
                         db =12,
                         decode_responses=True,
                         password='try_123as_pass')#password='try_123as_pass'
    for short in SCHOOL_LIST:
        dpts=col2.find_one({'short':short})['dpts']
        for dpt in dpts:
            s=GetPaperAuthors(short,dpt)

            del db[short+dpt]
            for i in s:
        
                db.lpush(short+dpt,i)
            print(short,dpt,'NAME TO REDIS OK')

def NameToRedisTrim():#变更host
    db1=redis.StrictRedis(host='localhost',#host='localhost'host='123.206.177.39'
                         port='6379',
                         db =11,
                         decode_responses=True,
                         password='try_123as_pass')#password='try_123as_pass'
    db2=redis.StrictRedis(host='localhost',#host='localhost'host='123.206.177.39'
                         port='6379',
                         db =12,
                         decode_responses=True,
                         password='try_123as_pass')#password='try_123as_pass'
    db3=redis.StrictRedis(host='localhost',#host='localhost'host='123.206.177.39'
                         port='6379',
                         db =13,
                         decode_responses=True,
                         password='try_123as_pass')#password='try_123as_pass'

    for key in db2.keys():
        for name in db2.lrange(key,0,db2.llen(key)):
            if name not in db1.lrange(key,0,db2.llen(key)):
                db3.lpush(key,name)
            
        print(key,'Trim OK')
def toRemote():
    name=[]
    dblocal=redis.StrictRedis(host='localhost',#host='localhost'host='123.206.177.39'
                         port='6379',
                         db =13,
                         decode_responses=True,
                         password='try_123as_pass')#password='try_123as_pass'
    dbremote=redis.StrictRedis(host='61.227.119.50',#host='localhost'host='123.206.177.39'
                         port='6379',
                         db =13,
                         decode_responses=True,
                         password='try_123as_pass')#password='try_123as_pass'
    for short in SCHOOL_LIST:
        dpts=col2.find_one({'short':short})['dpts']
        
        for dpt in dpts:
            KEY=short+dpt
            del dbremote[KEY]
            L=dblocal.lrange(KEY,0,dblocal.llen(KEY))
            for i in L:
                dbremote.lpush(short+dpt,i)
            print(KEY,'PASS EXTRA OK')    
toRemote()

