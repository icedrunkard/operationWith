import requests
from bs4 import BeautifulSoup as bs
from xpinyin import Pinyin
from urllib.parse import urlencode
import pymongo
#from pyabuyun import proxies
client=pymongo.MongoClient('localhost',port=27009)
db=client['schools']
col=db['211_list']


def base_q_ch(name,school):
    p=Pinyin()
    base_string='inurl:/in intitle:({name_ch} | {pinyin}) {school_ch}'
    i=col.find_one({'name':school})
    if i:
        s=base_string.format(name_ch=name,pinyin=p.get_pinyin(name,''),school_ch=school)

        return s
    else:
        s=base_string.format(name_ch=name,pinyin=p.get_pinyin(name,''),school_ch='')

        return s




def base_q_en(name,school):
    p=Pinyin()
    base_string='inurl:/in/ intitle:({name_ch} | {pinyin}) {school_en}'
    i=col.find_one({'name':school})
    if i:
        s=base_string.format(name_ch=name,pinyin=p.get_pinyin(name,''),school_en=i['name_en'])

        return s
    else:
        s=base_string.format(name_ch=name,pinyin=p.get_pinyin(name,''),school_en='')

        return s
