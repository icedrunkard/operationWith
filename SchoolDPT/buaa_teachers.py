# -*- coding: utf8 -*-

# 已爬取成功
from buaasce import html
import pymongo
import requests
import bs4
from bs4 import BeautifulSoup as bs
import re
from lxml import etree
client = pymongo.MongoClient('localhost:27009')
db = client['BUAA']


def parse_sce():
    dpt_name='化学学院_teachers'
    col=db[dpt_name]
    root='http://sce.buaa.edu.cn'
    for html_doc in html:
        soup=bs(html_doc,'lxml')
        Field=[]
        num=1
        for i in range(0,len(soup.find_all('tr')),2):
            if '：' in soup.find_all('tr')[i].a.get_text():
                name=soup.find_all('tr')[i].a.get_text(strip=True).split('：')[0]
                title=soup.find_all('tr')[i].a.get_text(strip=True).split('：')[1].replace('\t','').replace(' ','')
                url=root+soup.find_all('tr')[i].a.attrs['href']
                print(num,name,'==',title,'-',url)#title.encode('utf-8'),
                item={'name':name,
                      'title':title,
                      'url':url}
                col.update({'name':item['name']},item,True)
                num+=1

        

#parse_sce()

