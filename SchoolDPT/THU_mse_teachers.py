# -*- coding: utf8 -*-

# 已爬取成功
import pymongo

import requests

from bs4 import BeautifulSoup as BS

client = pymongo.MongoClient('localhost:27017')
db = client['THU']
col=db['mse_teachers']

urls=[
'http://www.mse.tsinghua.edu.cn//publish/mse/67/index.html',
'http://www.mse.tsinghua.edu.cn//publish/mse/72/index.html',
'http://www.mse.tsinghua.edu.cn//publish/mse/74/index.html',
'http://www.mse.tsinghua.edu.cn//publish/mse/75/index.html',
'http://www.mse.tsinghua.edu.cn//publish/mse/77/index.html',
'http://www.mse.tsinghua.edu.cn//publish/mse/78/index.html',

    ]

url_r="http://www.mse.tsinghua.edu.cn/publish/mse/79/index.html"
info_list=[]

i=0
for url in urls:
    
    r=requests.get(url)
    soup=BS(r.text,'lxml')

    for item in soup.find_all('td',valign=True):
        name=str(item.get_text().encode('raw_unicode_escape').decode('utf8','backslashreplace').replace('\\xa0','').replace(' ',''))


        
        if name:
            info={'id':i,

            'name':name,
            }
            if item.a:

                info['url']="http://www.mse.tsinghua.edu.cn"+item.a.attrs['href']

            col.insert(info)
            info_list.append(info)
            i+=1
print(i,len(info_list))
for item in info_list:

    print(item['name'])

r=requests.get(url_r)
soup=BS(r.text,'lxml')

for item in soup.find_all('div',class_="box_detail clear"):
    items=item.get_text().encode('raw_unicode_escape').decode('utf8','ignore').replace('\u3000','').split('，')
    for element in items:
        info={"id":i,'name':element,'tag':'retired'}#'离退休人员白新桂'已在数据库中修改
        col.insert(info)
        print(info)
        i+=1
