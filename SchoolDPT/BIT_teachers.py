# -*- coding: utf8 -*-

# 已爬取成功

import pymongo
import requests
import bs4
from bs4 import BeautifulSoup as bs
import re
from lxml import etree
client = pymongo.MongoClient('localhost:27009')
db = client['BIT']


def parse_chem():
    dpt_name='化学学院_teachers'
    col=db[dpt_name]
    urls=['http://cce.bit.edu.cn/szll/sssds/index.htm',
          'http://cce.bit.edu.cn/szll/bssds/index.htm']
    Field=[]
    Title=['硕士生导师','博士生导师']

    root=['http://cce.bit.edu.cn/szll/sssds/',
          'http://cce.bit.edu.cn/szll/bssds/',
          'http://cce.bit.edu.cn']
    for i in range(len(urls)):
        r=requests.get(urls[i])
        r.encoding='UTF-8'
        soup=bs(r.text,'lxml')

        for a in soup.find('div',class_='list09').find_all('a'):


            if re.search('.pdf',a.attrs['href']):
                url=root[2]+a.attrs['href'].replace('../..','')
            else:
                url=root[i]+a.attrs['href']
            title=Title[i]
            name=a.attrs['title']
            print(name,url,title)
            
        
            

    

            item={'name':name,
                          'title':title,
                          'url':url,
                          #'field':field
                  }
            #col.update({'name':item['name']},item,True)
            col.insert(item)


        

#parse_chem()

