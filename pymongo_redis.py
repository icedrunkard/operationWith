# -*- coding: utf8 -*-
import pymongo
import redis

client = pymongo.MongoClient('localhost:27009')
db = client['THU']
col=db['化学工程系_papers']


def GetPaperAuthors():
    s=set()
    for i in col.find():
        for a in i['author']:
            s.add(a['name'])
    return s




def ToRedis():
    db=redis.StrictRedis(host='localhost',port='6379',db = 2,decode_responses=True,)
    s=GetPaperAuthors()
    for i in s:
        db.set(i,i)
    print('set to redis FINISHED')
ToRedis()
