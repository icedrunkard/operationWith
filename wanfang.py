# -*- coding: utf-8 -*-
import requests
import json
import random


headers={
'Accept':'*/*',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
'Connection':'keep-alive',
'Content-Length':'342',
'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
'DNT':'1',
'Host':'new.wanfangdata.com.cn',
'Origin':'http://new.wanfangdata.com.cn',
'Referer':'http://new.wanfangdata.com.cn/searchResult/getAdvancedSearch.do',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36',
'X-Requested-With':'XMLHttpRequest',




        }

playload={
'paramStrs':'($language:chi+$language:en+$language:fre+$language:ger+$language:rus)*作者单位:(清华大学)',
'startDate':'2006',
'endDate':'2017',
'updateDate':'all',
'classType':'perio-perio_artical,degree-degree_artical,conference-conf_artical',
'pageNum':'0',
'pageSize':'20',
'sortFiled':'',
        }
d=round(random.random(),10)
print(d)
url='http://new.wanfangdata.com.cn/searchResult/getCoreSearch.do?'+str(d)

r=requests.post(url,headers=headers,data=playload)

j=json.loads(r.text)
for i in j.get('pageRow'):

    print(i['title'],i['authors_name'])
