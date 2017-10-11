# -*- coding: utf-8 -*-
from scrapy import Request,Spider
import re
from bs4 import BeautifulSoup as bs
from urllib.parse import urlencode
from googles.items import GooglesItem
from googles.get_google_links import base_q_ch,base_q_en
import pymongo


client=pymongo.MongoClient('localhost',port=27009)
db=client['THU']
col=db['mse_papers']


class GsSpider(Spider):    
    name = 'gss'
    allowed_domains = ['baidu.com','baiducontent.com','linkedin.com']
    base_url='https://www.baidu.com/s?{}'
    
    def start_requests(self):
        s=set()
        for i in col.find():
            for a in i['author']:
                s.add(a['name'])
        print('-'*20,len(s),'-'*20)
        for each in s:
            payload={'wd':base_q_ch(each,''),
                        'si':'cn.linkedin.com',
                        'ct':'2097152',
                        'tn':'baiduhome_pg',
                        'cl':'0'
                            }

            info=urlencode(payload)                
         
            yield Request(self.base_url.format(info),meta={'key':each})



    def parse(self, response):
        key=response.meta['key']
        soup=bs(response.text,'lxml')
        if soup.find_all('h3',class_='t'):
            for piece in soup.find_all('div',class_="result c-container "):
                if piece.find('h3',class_='t') and piece.find('a',class_='m'):
                    url=piece.find('a',class_='m').attrs['href']

                    #访问百度快照链接                
                    yield Request(url,meta={'key':key},callback=self.parse_baiducache)

            if soup.find('a',text=re.compile("下一页")):
                page_next='https://www.baidu.com'+soup.find('a',text=re.compile("下一页")).attrs['href']
                yield Request(page_next,meta={'key':key},callback=self.parse)
        else:
            print('--------------  no results found ---------------')




    
    def parse_baiducache(self,response):#此函数分析百度快照页面
        key=response.meta['key']
        item=GooglesItem()
                
        #百度快照页面编码更改，确保网址解析正确
        content=str(response.body, 'utf-8',errors='replace')
        soup=bs(content,'lxml')
        if soup.find('base'):
            url=soup.find('base').attrs['href']        
            item['url']=url
            yield Request(url,meta={'item':item,'key':key},callback=self.parse_linkedin)

    def parse_linkedin(self,response):
        item=response.meta['item']
        soup=bs(response.text,'lxml')
        if soup.find('section',id='groups'):
            if soup.find('section',id='groups').strong:
                item['name']=soup.find('section',id='groups').strong.get_text(strip=True)
            else:
                item['name']=response.meta['key']
        if soup.find_all('li',class_='position'):#section[experience>ul[positions:
            item['experience']=[]
            for piece in soup.find_all('li',class_='position'):

                exp={}

                #公司名称以书写版和领英版都要有,logo部分是领英给出的，item-subtitle是自己写的
                if piece.find('h5',class_='logo'):
                    company_url_ly=piece.find('h5',class_='logo').a.attrs['href']
                    company_name_ly=piece.find('h5',class_='logo').a.img.attrs['alt']
                    exp['company_url_ly']=company_url_ly
                    exp['company_name_ly']=company_name_ly
                if piece.find('h5',class_='item-subtitle'):
                    company_name=piece.find('h5',class_='item-subtitle').get_text()
                    exp['company_name']=company_name
                    if piece.find('h4',class_='item-title'):
                        position_title=piece.find('h4',class_='item-title').get_text()
                        exp['position_title']=position_title
                    if piece.find('h5',class_='item-subtitle').a:
                        if 'href' in piece.find('h5',class_='item-subtitle').a.attrs:
                            company_url_ha=piece.find('h5',class_='item-subtitle').a.attrs['href']
                            exp['company_url_ha']=company_url_ha
                if piece.find('span',class_='date-range'):#company
                    date_range=piece.find('span',class_='date-range').get_text(strip=True).split('(')[0].split('-')
                    exp['date_range']=date_range
                if piece.find('span',class_='location'):#company
                    location=piece.find('span',class_='location').get_text()
                    exp['location']=location

                item['experience'].append(exp)


                
        if soup.find_all('li',class_='school'):#section[education>ul[schools:
            item['education']=[]
            for piece in soup.find_all('li',class_='school'):
                
                edu={}
                
                if piece.find('h5',class_='logo'):
                    school_url_ly=piece.find('h5',class_='logo').a.attrs['href']
                    school_name_ly=piece.find('h5',class_='logo').a.img.attrs['alt']
                    edu['school_url_ly']=school_url_ly
                    edu['school_name_ly']=school_name_ly
                if piece.find('h4',class_='item-title'):
                    school_name=piece.find('h4',class_='item-title').get_text()
                    edu['school_name']=school_name
                    if piece.find('h4',class_='item-title').a: 
                        school_url=piece.find('h4',class_='item-title').a.attrs['href']
                        edu['school_url']=school_url
                if piece.find('h5',class_='item-subtitle'):
                    if piece.find('h5',class_='item-subtitle').find('span',class_='original translation'):                                       
                        degree_name=piece.find('h5',class_='item-subtitle').find('span',class_='original translation').get_text()
                        edu['degree_name']=degree_name
                if piece.find('span',class_='date-range'):
                    date_range=piece.find('span',class_='date-range').get_text()
                    edu['date_range']=date_range
                if piece.find('div',class_='description'):
                    if piece.find('div',class_='description').p:
                        description=[]
                        for pi in piece.find('div',class_='description').find_all('p'):
                            description.append(pi.get_text(strip=True))
                            edu['description']=description

                item['education'].append(edu)

            
        if soup.find('section',id='publications'):
            pass

        if soup.find('section',id='projects'):
            pass

        if soup.find('section',id='awards'):
            pass

        if soup.find('section',id='skills'):
            pass

        if soup.find('section',id='languages'):
            pass

        if soup.find('section',id='scores'):
            pass

        if soup.find('section',id='certifications'):
            pass



        yield item
