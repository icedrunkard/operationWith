import requests
from bs4 import BeautifulSoup as bs
from xpinyin import Pinyin
from urllib.parse import urlencode
import pymongo
from pyabuyun import proxies
client=pymongo.MongoClient('localhost',port=27009)
db=client['schools']
col=db['211_list']

base_url='https://www.xichuan.pub/search?{}&filter=0'
headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'}


name=''
school='中南大学'

def base_q(name,school):
    p=Pinyin()
    base_string='inurl:cn.linkedin.com/in/ intitle:({name_ch} | {pinyin}) ({school_ch} | {school_en})'
    i=col.find_one({'name':school})
    if i:
        s=base_string.format(name_ch=name,pinyin=p.get_pinyin(name,''),school_ch=school,school_en=i['name_en'])

        return s
    else:
        return None

payload={'q':base_q(name,school)}
info=urlencode(payload)

def get_google_links(info):
    r = requests.get(base_url.format(info),headers=headers,proxies=proxies)#
    soup=bs(r.text,'lxml')
    if soup.find_all('h3',class_='r'):
        for piece in soup.select('a[href*="//cn.linkedin.com/in/"]'):
            print(piece.get_text())
            print(piece.attrs['href'].replace('https://','http://'))
        if soup.find('a',class_='pn'):
            page_next='https://www.xichuan.pub'+soup.find('a',class_='pn').attrs['href']
            print(page_next)



get_google_links(info)
