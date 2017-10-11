# -*- coding:utf-8 -*-
import os
import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import quote_plus,quote,unquote_plus,unquote
import time
from headersText import genHeaders
from qText import query
import redis
from requests.auth import HTTPBasicAuth

db=redis.StrictRedis(host='localhost',port='6379',db = 0,decode_responses=True,password='try_123as_pass')
p= [db.get(key) for key in db.keys()]
print(p)
proxies = {
  "http": "http://"+p[0],
  "https": "https://"+p[0],
}
base='https://iced:runk@vip.kuaimen.bid/search'
#base='https://c3.hntvchina.com/search'

def loop(i):
    payload={
    'q':query('王祥','中南大学')[1],
    'filter':0,
    }
    #print(payload['q'])
    url=base+'?q='+quote_plus(payload['q'])

    r=requests.get(base,params=payload,proxies=proxies)
    print(r.status_code)
    #r.encoding='UTF-8'
    soup=bs(r.text,'lxml')

    for piece in soup.find_all('div',class_="g"):

        if piece.find('h3',class_='r') and piece.a:
            url=piece.a.attrs['href'].split('q=')[-1].split('&')[0]
        print(i,'   ',unquote(unquote(unquote(url))))
for i in range(2000):
    loop(i)
