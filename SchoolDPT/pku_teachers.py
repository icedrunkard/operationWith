# -*- coding: utf8 -*-

# 已爬取成功
from pkuccme import html
import pymongo
import requests
import bs4
from bs4 import BeautifulSoup as bs
import re
from lxml import etree
client = pymongo.MongoClient('localhost:27009')
db = client['PKU']

def parse_ccme():
    dpt_name='化学与分子工程学院_teachers'
    col=db[dpt_name]
    root='http://www.chem.pku.edu.cn'
    soup=bs(html,'lxml')
    for tr in soup.find_all('tr',bgcolor=False):
        for t in tr.next_siblings:
            if t.name=='tr':
                if not t.find('td',colspan=True):
                    for each in t.find_all('td'):
                        if each.a and 'href' in each.a.attrs and each.a.get_text():
                            name=each.a.get_text(strip=True).replace('\xa0','').replace('\u3000','').replace(' ','')
                            field=tr.get_text(strip=True)
                            url=root+each.a.attrs['href']
                            print('-',name,url,field)
                            item={'name':name,
                                  'url':url,
                                  'field':field}
                            col.insert(item)
                else :
                    break
            else:
                continue
                
        

#parse_ccme()

