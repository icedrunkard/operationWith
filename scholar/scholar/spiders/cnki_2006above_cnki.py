# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy
from random import random
from scholar.items import ScholarItem,Scholar2Item
from bs4 import BeautifulSoup as bs



#url是大学集合页面网址，每页有20条大学
url='http://navi.cnki.net/knavi/Common/Search/PPaper'

#paper_url是某大学所有学位论文集合页面，每页有20条学位论文
paper_url_1st='http://navi.cnki.net/knavi/PPaperDetail/GetArticleBySubject'
paper_url_2nd='http://navi.cnki.net/knavi/PPaperDetail/GetArticleBySubjectinPage'
#playload1是请求大学集合页面所提交的数据
playload_1={
        'SearchStateJson':'{"StateID":"","Platfrom":"","QueryTime":"","Account":"knavi","ClientToken":"","Language":"","CNode":{"PCode":"CDMD","SMode":"","OperateT":""},"QNode":{"SelectT":"","Select_Fields":"","S_DBCodes":"","QGroup":[],"OrderBy":"RT|","GroupBy":"","Additon":""}}',
        'displaymode':'2',
        'pageindex':'1',#页码
        'pagecount':'20',
        'index':'1',

        }

#playload2是请求某大学所有学位论文集合页面所提交的数据
playload_2={
        'pcode':'',#需添加学校pcode，即school_pcode
        'baseID':'',#需添加学校代码，即school_baseid
        'subCode':'',
        'orderBy':'YE|DESC',#按学位年度降序排列
        'scope':'%u5168%u90E8'
        }

#共有776所大学，每页20所，共39页
page_school=39

class CnkiSpider(scrapy.Spider):
    name = "cnki"
    allowed_domains = ["cnki.net"]
    def start_requests(self):
        #=================================================================
        #
        #   776个大学，共39个页面，为了与页码一致，range(1,page_school+1),合计815个POST
        #
        #=================================================================
        for i in range(1,page_school+1):
            num=round(random(),16)
            playload_1['pageindex']=str(i)
            playload_1['random']=str(num)

            yield scrapy.FormRequest(url,formdata=playload_1,callback=self.parse)

    def parse(self,response):
        #此函数分析学校的集合页面
        item=ScholarItem()
        item['key']=0
        soup=bs(response.text,'lxml')
        bsoj=soup.find('ul',class_="list_tab").findAll('li',class_=False)
        #学校页面range(len(bsoj))
        for i in range(len(bsoj)):
            
            school_baseid=bsoj[i].a.attrs['href'].split('=')[-1]
            school_pcode=bsoj[i].a.attrs['href'].split('&')[-2].split('=')[-1]


            playload_2['baseID']=school_baseid
            playload_2['pcode']=school_pcode

            item['school_pcode']=school_pcode           
            item['school_baseid']=school_baseid
            item['school_name']=bsoj[i].find('h2').get_text(strip=True)
            item['school_location']=bsoj[i].find('span',class_='tab_3').get_text(strip=True)
            page=int(int(bsoj[i].find('span',class_='tab_4').get_text(strip=True))/20)+1
            item['paper_pages']=page
            item['school_title']=[]
            if bsoj[i].select('span div font'):
                item['school_title']=[x.get_text(strip=True) for x in bsoj[i].select('span div font')]

            item['playload']=deepcopy(playload_2)

                #第一页请求网址为‘getbysubject’
                
            yield scrapy.FormRequest(paper_url_1st,meta={'item':deepcopy(item),},formdata=playload_2,callback=self.parse2)



            
    def parse2(self,response):

        #此函数得到学校的论文集合页面
        item=response.meta['item']
        p=item['key']
        playload_2=item['playload']        

        #确定论文共有多少页（每页20条）
        paper_pages=item['paper_pages']
        #print(item['school_baseid'],paper_pages,'total')

        soup=bs(response.text,'lxml')
        
        #文章被包在有“class”属性的‘tr’标签里
        bsoj=soup('tr')#等价于soup.findAll('tr')

        for i in range(1,len(bsoj)):#最后一个是bsoj[20]
            item2=Scholar2Item()

            item2['degree_year']=int(bsoj[i].find('td',align=True).get_text(strip=True))

            #只获取10年以内的论文
            if item2['degree_year']<2006:
                break

            
            item2['school_title']=item['school_title']
            item2['school_name']=item['school_name']
            item2['school_location']=item['school_location']
            item2['school_baseid']=item['school_baseid']
            item2['school_pcode']=item['school_pcode']
            item2['paper_pages']=item['paper_pages']
            
            paper_path=bsoj[i].find('a',onclick=True).attrs['onclick'].split("'")[3]
            
            item2['paper_path']=paper_path
            
            item2['degree']=bsoj[i].findAll('td',align=True)[1].get_text(strip=True)
            item2['author']=bsoj[i].findAll('td',title=True)[0].get_text(strip=True)

            #导师可能是多个人，加split(';')变成列表
            item2['tutor']=bsoj[i].findAll('td',title=True)[1].get_text(strip=True).split(';')

            yield scrapy.Request(paper_path,meta={'item2':deepcopy(item2)},callback=self.parse3)

        else:
            p+=1
            if p<paper_pages:#实际页数减1
                playload_2['pIdx']=str(p)
                item['playload']=playload_2
                item['key']=p

                #print('posting...',playload_2['baseID'],playload_2['pIdx'],'-----now------')
                yield scrapy.FormRequest(paper_url_2nd,meta={'item':deepcopy(item)},formdata=playload_2,callback=self.parse2)



        
    def parse3(self,response):

        item2=response.meta['item2']
        
        #关键词和中图分类号都可能是多个值
        item2['keywords']=[]
        item2['udc']=[]
        soup=bs(response.text,'lxml')
        bsoj=soup.find('div',class_="wxBaseinfo")

        item2['paper_name']=soup.title.get_text(strip=True).split('-')[0]

        if bsoj.find('label', id="catalog_KEYWORD"):
            keywords_tag=bsoj.find('label', id="catalog_KEYWORD").parent
            keywords_tag.label.replace_with('')
            keywords=keywords_tag.get_text(strip=True).split(';')
            while '' in keywords:
                keywords.remove('')
            item2['keywords']=keywords


        if bsoj.find('label', id="catalog_ZTCLS"):
            udc_tag=bsoj.find('label', id="catalog_ZTCLS").parent
            udc_tag.label.replace_with('')
            udc=udc_tag.get_text(strip=True).split(';')
            while '' in udc:
                udc.remove('')
            item2['udc']=udc

        yield item2

    def parse4(self,response):
        pass
