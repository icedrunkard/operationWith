import requests
from bs4 import BeautifulSoup as pybs
from urllib.parse import urlencode
import re
import pymongo
from school_211_list import *
from CODES import CODES

client=pymongo.MongoClient('localhost',port=27009)
db=client['schools']
col0=db['211_list']
col=db['names']
col2=db['list']
col3=db['codes']
def get_schoolname():
    s=[]
    url='http://t3.zsedu.net/ulink/main.html'
    r=requests.get(url)
    print(r.encoding)
    soup=pybs(r.text,'lxml')
    for i in soup.find_all('td',)[46:]:
        if i.a:
            if 'href' in i.a.attrs:
                
                name=i.a.get_text(strip=True).encode('ISO-8859-1','ignore').decode('gb2312','ignore')
                link=i.a.attrs['href']
                
                
                c={'name':name,'link':link}
                if i.find('span',class_='size12'):
                    c['title']=i.find('span',class_='size12').get_text(strip=True).replace('[','').replace(']','').split('/')
                print(c)
                col.insert(c)
    return s

def get_id(name):
    keywords='inurl:cn.linkedin.com/edu/ site:cn.linkedin.com intitle:{}|领英'
    payload={'wd':keywords.format(name),}
    url='http://www.baidu.com/s?'+urlencode(payload)
    r=requests.get(url)

    #找到链接列表
    m=re.search(r'bds.comm.iaurl=(.*?)]',r.text)
    if m:
        searchobj=m.group()

    #取出大学可能的代码
        s=set()
        for i in re.finditer(r'(\-)(\d{5})',searchobj):

            s.add(i.group(2))
        return s    #,len(s)
def getCodes():
    k=0
    for i in re.finditer(r'(.*?)([0-9]+)',CODES):
        
        if i.group(1):
            k+=1
            print(k,i.group(1),i.group(2).strip('\n'))
            col3.insert({
                'school_name':i.group(1),
                'linkedinCode':i.group(2).strip('\n')
                })
        
    #print(m.group())
def school_title():
    k=0
    for i in col.find():
        if 'title' in i.keys():
            #s=get_id(i['name'])
            k+=1
            if col0.find({'school_name_ch':i['name']}).count()>0:
                for item in col0.find({'school_name_ch':i['name']}):
                    col2.insert({
                        'name':i['name'],
                        'title':i['title'],
                        'name_en':item['school_name_en'],
                        'link':i['link']
                        })
            else:
                print(i['name'],'no matches,====================')

def get_names_en():
    k=0
    for i in re.finditer(r'(.*?)([a-z\s\-\/\&A-Z]+)',names):
        
        if i.group(1):
            k+=1
            print(k,i.group(1),i.group(2).strip('\n'))
            col0.insert({
                'school_name_ch':i.group(1),
                'school_name_en':i.group(2).strip('\n')
                })

getCodes()
