# -*- coding: utf8 -*-

# 已爬取成功

import pymongo
import requests
import bs4
from bs4 import BeautifulSoup as bs
import re
from lxml import etree
client = pymongo.MongoClient('localhost:27009')
db = client['TONGJI']


def parse_chem():
    dpt_name='化学科学与工程学院_teachers'
    col=db[dpt_name]
    urls=['http://chemweb.tongji.edu.cn/content.aspx?info_lb=792&flag=699',
          'http://chemweb.tongji.edu.cn/content.aspx?info_lb=793&flag=699',
          'http://chemweb.tongji.edu.cn/content.aspx?info_lb=794&flag=699']
    Field=[]
    Title=['教授','副教授','讲师']


    for i in range(len(urls)):
        r=requests.get(urls[i])
        r.encoding='UTF-8'
        soup=bs(r.text,'lxml')
        #print('---------------')
        for a in soup.find('table',align='center').find_all('a'):

            url=a.attrs['href']
            title=Title[i]
            name=a.get_text(strip=True).replace(' ','').replace('\xa0','')
            print(name,title,url)
            
        
            

    

            item={'name':name,
                          'title':title,
                          'url':url,
                          #'field':field
                  }
            col.update({'url':item['url']},item,True)
            #col.insert(item)


        

parse_chem()

