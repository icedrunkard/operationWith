# -*- coding: utf-8 -*-
from titleText import inTitle
import pymongo
#from pyabuyun import proxies


client=pymongo.MongoClient('localhost',port=27009)
db=client['schools']
col=db['list_211985']



#google输入参数
def query(name,school):
    s='intitle:{title} site:cn.linkedin.com intext:{school_ch} | {school_en}'
    item=col.find_one({'name':school})
    Qset=[]
    for i in inTitle(name):
        q=s.format(title=i,school_ch=school,school_en=item['name_en'])
        Qset.append(q)
    return Qset

#print(query('王祥','中南大学'))
    
