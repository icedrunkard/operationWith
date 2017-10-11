# -*- coding: cp936 -*-
import pymongo
import re

client = pymongo.MongoClient('localhost:27009')
db = client['THU']
db2=client['XMU']
col= db['mse_students']
col2=db['mse_s1']
col3=db2['化学化工学院_teachers']
def PullValid():
    i=0
    for item in col.find():
        if 'education' in item.keys():
            for part in item['education']:
                if 'date_range' in part.keys():
                    part['date_range']=part['date_range'].replace(' ','').replace('年','')



            col2.insert(item)
            i+=1

    print(i)

#print(db2.collection_names())


def ss():
    s=set()
    for name in db2.collection_names():
        if re.search('teachers', name):
            for i in db2[name].find():
                if i['name'] not in s:
                    s.add(i['name'])
                    if 'field' in i.keys():
                        i.pop('_id')
                        col3.insert(i)
                    else:
                        g=i
                        g.pop('_id')
                        g['filed']=name.replace('_teachers','')
                        col3.insert(g)
def namecount():
    s=set()
    for i in col3.find():
        s.add(i['name'])
    print(len(s))


ss()
namecount()
