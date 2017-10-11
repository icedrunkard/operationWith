# -*- coding: utf8 -*-

# 已爬取成功
#from BNUchem import html
import pymongo
import requests
import bs4
from bs4 import BeautifulSoup as bs
import re
from lxml import etree
client = pymongo.MongoClient('localhost:27009')
db = client['BNU']


def parse_chem():
    dpt_name='化学学院_teachers'
    col=db[dpt_name]
    urls=['http://www.chem.bnu.edu.cn/szll/jsdw/wjhxyjs/',
          'http://www.chem.bnu.edu.cn/szll/jsdw/fxhxyjs/',
          'http://www.chem.bnu.edu.cn/szll/jsdw/yjhxyjs/',
          'http://www.chem.bnu.edu.cn/szll/jsdw/llhwlhxyjs/',
          'http://www.chem.bnu.edu.cn/szll/jsdw/gfzhxywlyjs1/',
          'http://www.chem.bnu.edu.cn/szll/jsdw/yyhxyjs/',
          'http://www.chem.bnu.edu.cn/szll/jsdw/fsxywhxx1/',
          'http://www.chem.bnu.edu.cn/szll/jsdw/hxjyyjs/',
          'http://www.chem.bnu.edu.cn/szll/jsdw/hxswxx/',
          'http://www.chem.bnu.edu.cn/szll/jsdw/hxsyjxzx1/']
    Field=[]

    for i in range(len(urls)):
        r=requests.get(urls[i])
        r.encoding='UTF-8'
        soup=bs(r.text,'lxml')
        field=soup.find('table',width='95%').tr.get_text(strip=True).replace(' ','').replace('\xa0','').split(':')[-1]
        Field.append(field)
        Title=[]
        for t in range(0,len(soup.find('table',width='95%').table.find_all('tr')),2):

            title=soup.find('table',width='95%').table.find_all('tr')[t].get_text(strip=True).replace(' ','').replace('\xa0','')
            Title.append(title)
            for k in range(1,len(soup.find('table',width='95%').table.find_all('tr')),2):
                for a in soup.find('table',width='95%').table.find_all('tr')[k].find_all('a'):
                    url=urls[i]+a.attrs['href']
                    name=a.attrs['title']
                    print(name,'--',title,'--',field)
            
        
            

    

                    item={'name':name,
                          'title':title,
                          'url':url,
                          'field':field}
                    col.update({'name':item['name']},item,True)


        

parse_chem()

