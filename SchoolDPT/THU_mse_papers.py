# -*- coding: utf8 -*-

# 
import pymongo



client = pymongo.MongoClient('localhost:27009')
db = client['THU']
colpapers=db['mse_papers']
colteachers=db['mse_teachers']

teachers=set()

for i in colteachers.find():
    i['name']
    authors=set()
    for j in colpapers.find({'tutor':i['name']}):
        for author in j['author']:
            authors.add(author['name'])
    print(authors)
    
