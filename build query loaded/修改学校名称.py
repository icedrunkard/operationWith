# -*- coding:utf-8 -*-
import pymongo

client=pymongo.MongoClient('localhost',port=27009)
db=client['schools']
col211985=db['list_211985']
colinkcodes=db['985_codes']
coldpts=db['dpts_985']

def zhenghe():
    for i in col211985.find():
        item=coldpts.find_one({'university':i['name']})
        if item:
            
        
        
            print(item.keys())
            for key in item.keys():
                if key not in i.keys():
                    i[key]=item[key]
            col211985.update({'name':i['name']},i,True)



zhenghe()
