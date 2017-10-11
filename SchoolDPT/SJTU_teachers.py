# -*- coding: utf8 -*-

# 已爬取成功

import pymongo
import requests
import bs4
from bs4 import BeautifulSoup as bs
import re
from lxml import etree
client = pymongo.MongoClient('localhost:27009')
db = client['SJTU']


def parse_chem():
    dpt_name='化学化工学院_teachers'
    col=db[dpt_name]
    url='http://scce.sjtu.edu.cn/jiaoshi.php?c=3'
    Field=[]
    

    root='http://scce.sjtu.edu.cn/jiaoshi.php'
    r=requests.get(url)
    r.encoding='UTF-8'
    soup=bs(r.text,'lxml')
    ul=soup.find('ul',class_='people_list2')
    for i in range(len(ul.find_all('li',style=True))):
        Field.append(ul.find_all('li',style=True)[i].get_text(strip=True))


    for k in range(len(ul.find_all('li',style=False))):#k对应i
        for dl in ul.find_all('li',style=False)[k].find_all('dl'):
            title=dl.dt.get_text(strip=True)
            for a in dl.find_all('a'):
                url=root+a.attrs['href']
                name=a.attrs['title'].replace(' ','')
        

                print(name,Field[k],title)
            
        
            

    

                item={'name':name,
                          'title':title,
                          'url':url,
                          'field':Field[k]
                  }
                col.update({'url':item['url']},item,True)
                #col.insert(item)


        

parse_chem()

