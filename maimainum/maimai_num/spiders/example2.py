#-*- coding:utf-8 -*-

import requests
import urllib
import json

from scrapy import Spider, Request
from maimai_num.items import MaimaiNumItem

import random

#从14000001开始爬取
count=29000000

#本次准备爬取130万条，130万=a*b*c
a=100
b=200
c=350



class ExampleSpider(Spider):
    name = "example2"
    allowed_domains = ['maimai.cn']
    url_start = 'https://maimai.cn/contact/interest_contact/{id}?jsononly=1'
    def start_requests(self):
        for i in range(1,a+1):
            yield Request(self.url_start.format(id=i),meta={'key':i},callback=self.parse)



    def parse(self,response):#分析用户在完整页面呈现的数据
        
        j=response.meta['key']
        j-=1
        for i in range(1,b+1):
            j_=j*b+i
            p=j_-1
            yield Request(self.url_start.format(id=j_),meta={'key':p},dont_filter=True,callback=self.parse2)
    def parse2(self,response):#分析用户在完整页面呈现的数据
        L=[]
        k=response.meta['key']
        for i in range(count+1,count+c+1):
            p=c*k+i
            L.append(p)

        for s in L:
            yield Request(self.url_start.format(id=s),meta={'key':s},dont_filter=True,callback=self.parse3)            

    def parse3(self,response):
        item=MaimaiNumItem()
        result=json.loads(response.text)
        
        if 'data' in result.keys():
            item['all']=result
            yield item
            s=response.meta['key']
            print(s)

            

