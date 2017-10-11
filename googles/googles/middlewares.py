# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import time
import redis
import random
import base64
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from googles.GetUserAgents_from_web import ua_list


"""----------------------------------------------------------"""
#abuyun代理服务器
proxyServer = "http://proxy.abuyun.com:9020"
# 代理隧道验证信息
proxyUser = "H264P9E9M949159D"
proxyPass = "1C6AED9CB122390C"
# for Python3
proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")
# for Python2
#proxyAuth = "Basic " + base64.b64encode(proxyUser + ":" + proxyPass)
"""----------------------------------------------------------"""
############################################################################################################################

"""=========================================================="""
#vps代理服务器
db=redis.StrictRedis(host='localhost',port='6379',db = 4,decode_responses=True,)
"""=========================================================="""

 

class AbuyunProxiesMiddleware(HttpProxyMiddleware):
    proxies = {}
    def __init__(self, auth_encoding='latin-1'):
        self.auth_encoding = auth_encoding
        
        self.proxies[proxyServer] = proxyUser + proxyPass

    def process_request(self, request, spider):
        request.meta["proxy"] = proxyServer
        request.headers["Proxy-Authorization"] = proxyAuth


    def process_response(self,request, response, spider):
        
        if response.status in [500,501,502,503,504,999]:
            time.sleep(20)
            return request
        else:
            return response
        
class VPSProxiesMiddleware(HttpProxyMiddleware):
    def process_request(self, request, spider):    
        if db.keys():
            proxies = [db.get(key) for key in db.keys()]
            request.meta["proxy"] = 'http://'+proxies[0]
        else:
            time.sleep(1)
    def process_response(self,request, response, spider):
        
        if response.status in [500,501,502,503,504,999]:
            time.sleep(10)
            return request
        else:
            return response

class RotateUserAgentMiddleware(UserAgentMiddleware):

    def __init__(self,user_agent):
        self.user_agent = ua_list
 
    def process_request(self, request, spider):
        #这句话用于随机选择user-agent
        ua = random.choice(self.user_agent)
        if ua:
            request.headers.setdefault('User-Agent', ua)
