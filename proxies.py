# -*- coding: cp936 -*-
import requests
import time

from bs4 import BeautifulSoup as bs


targetUrl = "http://city.ip138.com/ip2city.asp"
proxyHost = "proxy.abuyun.com"
proxyPort = "9020"

proxyUser = "H264P9E9M949159D"
proxyPass = "1C6AED9CB122390C"

proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
      "host" : proxyHost,
      "port" : proxyPort,
      "user" : proxyUser,
      "pass" : proxyPass,
    }

proxies = {
        "http"  : proxyMeta,
        "https" : proxyMeta,
    }
ip_pool=[]
while True:
        resp = requests.get(targetUrl, proxies=proxies)

        print(resp.text)
        soup=bs(resp.text,'lxml')
        if soup.center:
                ip=soup.center.get_text(strip=True).split('[')[-1].split(']')[0]
                valid_ip='http://'+str(ip)+':8080'
                pro={valid_ip}

                r=requests.get('http://www.baidu.com',proxies=pro)
                print(r.text)
                if r.status_code==200:

                                
                        valid_ip_=valid_ip+','
                                
                        print(valid_ip_)
                    
