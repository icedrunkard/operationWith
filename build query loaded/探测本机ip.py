# -*- coding:utf-8 -*-
import os
import requests
from bs4 import BeautifulSoup as bs
url='http://1212.ip138.com/ic.asp'
r=requests.get(url)
r.encoding='gb2312'
soup=bs(r.text,'lxml')
print(soup.center.get_text())
