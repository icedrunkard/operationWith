# -*- coding: utf8 -*-

# 已爬取成功

import pymongo
import requests
import bs4
from bs4 import BeautifulSoup as bs
import re
from lxml import etree
client = pymongo.MongoClient('localhost:27009')
db = client['ZJU']


def parse_chem():
    dpt_name='化学系_teachers'
    col=db[dpt_name]
    url='http://www.chem.zju.edu.cn/chinese/redir.php?catalog_id=471'
    Title=[]
    

    root='http://www.chem.zju.edu.cn/chinese/'
    r=requests.get(url)
    r.encoding='GB2312'
    soup=bs(r.text,'lxml')
    tb=soup.find_all('table',class_='list')
    for i in range(len(tb)):
        Title.append(tb[i].tr.get_text(strip=True))


    for k in range(len(tb)):#k对应i
        for a in tb[k].find_all('a'):
            title=Title[k]

            url=root+a.attrs['href']
            name=a.get_text(strip=True).replace(' ','').replace('\xa0','')
        

            print(name,title,url)
            

            item={'name':name,
                          'title':title,
                          'url':url,
                          #'field':Field[k]
                  }
            col.update({'url':item['url']},item,True)
                #col.insert(item)


def parse_ccbe():
    dpt_name='化学工程与生物工程_teachers'
    col=db[dpt_name]
    url='http://che.zju.edu.cn/cn/redir.php?catalog_id=61439'
    Field=[]
    

    root='http://che.zju.edu.cn/cn/'
    r=requests.get(url)
    r.encoding='GB2312'
    soup=bs(r.text,'lxml')
    div=soup.find_all('div',class_='con')
    for i in range(len(div)):
        Field.append(div[i].h3.get_text(strip=True))


    for k in range(len(div)):#k对应i
        for a in div[k].find_all('a'):
            field=Field[k]

            url=root+a.attrs['href']
            name=a.get_text(strip=True).replace(' ','').replace('\xa0','')
        

            print(name,field,url)
            

            item={'name':name,
                          #'title':title,
                          'url':url,
                          'field':Field[k]
                  }
            col.update({'url':item['url']},item,True)
                #col.insert(item)

        

#parse_chem()
#parse_ccbe()
