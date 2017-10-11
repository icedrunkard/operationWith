# -*- coding: utf8 -*-

# 已爬取成功
from renminchem import html
import pymongo
import requests
import bs4
from bs4 import BeautifulSoup as bs
import re
from lxml import etree
client = pymongo.MongoClient('localhost:27009')
db = client['RENMIN']

def parse_chem():
    dpt_name='化学系_teachers'
    col=db[dpt_name]
    root='http://chem.ruc.edu.cn/'
    soup=bs(html,'lxml')
    Field=[]
    i=0
    for p in soup.find_all('p'):
        Field.append(p.get_text(strip=True))
    for div in soup.find_all('div'):
        for a in div.find_all('a'):
            name=a.get_text(strip=True)
            url=root+a.attrs['href']
            field=Field[i]
            item={'name':name,
                  'url':url,
                  'field':field}
            print(name,field)
            col.insert(item)
        i+=1

                
        

parse_chem()

