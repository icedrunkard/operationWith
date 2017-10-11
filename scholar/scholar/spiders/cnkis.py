# -*- coding: utf-8 -*-
import scrapy

from scholar.items import ScholarItem
from bs4 import BeautifulSoup as bs



#url是大学集合页面网址，每页有20条大学
url='http://navi.cnki.net/knavi/Common/Search/PPaper'

#paper_url是某大学所有学位论文集合页面，每页有20条学位论文
paper_url='http://navi.cnki.net/knavi/PPaperDetail/GetArticleBySubject'

#playload1是请求大学集合页面所提交的数据
playload_1={
        'SearchStateJson':'{"StateID":"","Platfrom":"","QueryTime":"","Account":"knavi","ClientToken":"","Language":"","CNode":{"PCode":"CDMD","SMode":"","OperateT":""},"QNode":{"SelectT":"","Select_Fields":"","S_DBCodes":"","QGroup":[],"OrderBy":"RT|","GroupBy":"","Additon":""}}',
        'displaymode':'2',
        'pageindex':'1',#页码
        'pagecount':'20',
        'index':'1',
        #'random':'0.8793145890277527'
        }

#playload2是请求某大学所有学位论文集合页面所提交的数据
playload_2={
        'pcode':'CDMD',
        'baseID':'',#需添加学校代码，即school_code
        'subCode':'',
        'orderBy':'YE|DESC',#按学位年度降序排列
        
        }

#共有776所大学，每页20所，共39页
page_school=39

class CnkiSpider(scrapy.Spider):
    name = "cnkis"
    allowed_domains = ["cnki.net",""]
    def start_requests(self):
        #=================================================================
        #
        #776个大学，共39个页面，为了与页码一致，range(1,page_school+1)
        #
        #=================================================================
        for i in range(1,page_school+1):
            playload_1['pageindex']=str(i)
            yield scrapy.FormRequest(url,formdata=playload_1)

    def parse(self, response):

        #此函数得到学校的集合页面
        item=ScholarItem()
        soup=bs(response.text,'lxml')
        bsoj=soup.find('ul',class_="list_tab").findAll('li',class_=False)
        #学校页面range(len(bsoj))
        for i in range(len(bsoj)):
            

            item['school_name']=bsoj[i].find('h2').get_text(strip=True)
            item['school_url']=bsoj[i].find('span',class_='tab_4').get_text(strip=True)

            yield item
            yield scrapy.FormRequest(paper_url,meta={'item':item,'key':0,'playload':playload_2},formdata=playload_2,callback=self.parse)
        

            
    def parse2(self,response):

        #此函数得到学校的论文集合页面
        item=response.meta['item']
        p=response.meta['key']
        playlod_2=response.meta['playload']

        soup=bs(response.text,'lxml')
        
        #确定该学校论文页数
        page_paper=int(soup.find('span', id="partiallistcount2").get_text())


        #文章被包在有“class”属性的‘tr’标签里,比文章数多一个
        bsoj=soup('tr',class_=True)#等价于soup.findAll('tr')

        for i in range(len(bsoj)):
            item2=ScholarItem()
            item2['school_title']=item['school_title']
            item2['school_name']=item['school_name']
            item2['school_location']=item['school_location']
            item2['school_url']=item['school_url']
            #文章名称在第一个‘a’标签里
            item2['paper_name']=bsoj[i].a.get_text(strip=True)
            
            paper_path=bsoj[i].find('a',onclick=True).attrs['onclick'].split("'")[3]
            
            item2['paper_path']=paper_path
            item2['degree_year']=bsoj[i].findAll('td',align=True)[0].get_text(strip=True)
            item2['degree']=bsoj[i].findAll('td',align=True)[1].get_text(strip=True)
            item2['author']=bsoj[i].findAll('td',title=True)[0].get_text(strip=True)
            #导师可能是多个人，加split(';')变成列表
            item2['tutor']=bsoj[i].findAll('td',title=True)[1].get_text(strip=True).split(';')
            yield scrapy.Request(paper_path,meta={'item2':item2},callback=self.parse3)

        p+=1
        if p<page_paper:#实际页数减1
            playload_2['pIdx']=str(p) 
            yield scrapy.FormRequest(paper_url,meta={'item':item,'key':p,'playload':playload_2},formdata=playload_2,callback=self.parse2)
        
        
    def parse3(self,response):

        item2=response.meta['item2']
        item2['keywords']=[]
        item2['udc']=[]
        soup=bs(response.text,'lxml')
        bsoj=soup.find('div',class_="wxBaseinfo")
        
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
        #yield item2
