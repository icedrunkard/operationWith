# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html


import base64
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware



#ua_list=get_ua()
# 代理服务器
proxyServer = "http://proxy.abuyun.com:9010"

# 代理隧道验证信息
proxyUser = "H7394I09T0C1L82P"#"H264P9E9M949159D"
proxyPass = "427F77676DBAFF9F"#"1C6AED9CB122390C"

# for Python3
proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")

# for Python2
#proxyAuth = "Basic " + base64.b64encode(proxyUser + ":" + proxyPass)

 

class ScholarMiddleware(HttpProxyMiddleware):
    proxies = {}
    def __init__(self, auth_encoding='latin-1'):
        self.auth_encoding = auth_encoding
        
        self.proxies[proxyServer] = proxyUser + proxyPass

    def process_request(self, request, spider):
        request.meta["proxy"] = proxyServer
        request.headers["Proxy-Authorization"] = proxyAuth
        


