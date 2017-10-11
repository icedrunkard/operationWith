# -*- coding: utf-8 -*-
import requests
import pymongo
from urllib.parse import urlencode


client=pymongo.MongoClient('localhost',port=27009)
db=client['schools']
col=db['211_list']

headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36',
        }

def build_q():
        url_base='https://www.baidu.com/s?{}'
        base='inurl:cn.linkedin.com/edu/ intitle:(school)'
        c=[]
        for item in col.find():
                s=base.format(school=item['name'])
                payload={'word':s,
                        'si':'cn.linkedin.com',
                        'ct':'2097152',
                        'tn':'93012342_hao_pg'
                            }
                url=url_base+urlencode(playload)
                c.append(url)
        return c
c=build_q()
def getschoolcodes(c):
        for url in c:
                r=requests.get(url,headers=headers,proxies=proxies)
                r.encoding='utf-8'
                
