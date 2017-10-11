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
db = client['FUDAN']

def parse_chem():
    dpt_name='化学系_teachers'
    col=db[dpt_name]
    root='http://www.chemistry.fudan.edu.cn'
    soup=bs(html,'lxml')
    Field=['分析化学',
           '化学生物学',
           '无机化学',
           '有机化学',
           '物理化学']
    i=0
    urls=['http://www.chemistry.fudan.edu.cn/data/list/fxhx',
          'http://www.chemistry.fudan.edu.cn/data/list/hxswx',
          'http://www.chemistry.fudan.edu.cn/data/list/wjhx',
          'http://www.chemistry.fudan.edu.cn/data/list/yjhx',
          'http://www.chemistry.fudan.edu.cn/data/list/wlhx']
    for i in range(len(urls)):
        r=requests.get(urls[i])
        r.encoding='UTF-8'
        soup=bs(r.text,'lxml')
        for a in soup.find('div',class_="right-nr").find_all('a'):

            name=a.get_text(strip=True).replace('\xa0','').replace(' ','')
            url=root+a.attrs['href']
            field=Field[i]
            item={'name':name,
                  'url':url,
                  'field':field}
            print(name,field,url)
            col.insert(item)


                
        

parse_chem()

