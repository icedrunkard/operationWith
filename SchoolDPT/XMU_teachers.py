# -*- coding: utf8 -*-

# 已爬取成功

import pymongo
import requests
import bs4
from bs4 import BeautifulSoup as bs
import re
from lxml import etree
client = pymongo.MongoClient('localhost:27009')
db = client['XMU']


def parse_chem():
    dpt_name='化学工程与生物工程系_teachers'
    col=db[dpt_name]
    urls=['http://cbe.xmu.edu.cn/{}/list.htm'.format(str(i)) for i in range(11811,11817)]
    root='http://cbe.xmu.edu.cn'
    for url in urls:
        
        r=requests.get(url)
        r.encoding='UTF-8'
        soup=bs(r.text,'lxml')
        li=soup.find('ul',class_='cp').find_all('li')
        for i in range(len(li)):
            url=root+li[i].find_all('div')[1].a.attrs['href']
            piece=li[i].find_all('div')[1].a.get_text(',').split(',')
            name=piece[0]
            if not re.search('电话',piece[2]):
                title=piece[1]+piece[2]
            else:
                title=piece[1]
                    
            field=soup.title.get_text()

            print(field,name,title,url)
            

            item={'name':name,
                          'title':title,
                          'url':url,
                          'field':field
                  }
            col.update({'url':item['url']},item,True)
                #col.insert(item)


def parse_chembio():
    dpt_name='化学生物系_teachers'
    col=db[dpt_name]
    url='http://chembio.xmu.edu.cn/teachers.asp'
    Field=[]
    Title=[]
    

    root='http://chembio.xmu.edu.cn/'
    r=requests.get(url)
    r.encoding='UTF-8'
    soup=bs(r.text,'lxml')
    div_t=soup.find_all('div',class_='title')
    for i in range(len(div_t)):
        title=div_t[i].find_all('div')[1].get_text(strip=True)
        #print(div_t[i].next_siblings)
        for t in div_t[i].next_siblings:
            #print(t)
            if type(t)==bs4.element.NavigableString:
                continue
            elif t.find('table'):
                name=t.img.attrs['alt']
                url=root+t.a.attrs['href']
                print(name,title,url)
                item={'name':name,
                          'title':title,
                          'url':url,
                         # 'field':Field[k]
                  }
                col.update({'url':item['url']},item,True)
            elif t.find('div',class_='left'):
                break
            else:
                continue
def pcoss():
        
    dpt_name='固体表面物理化学国家重点实验室_teachers'
    col=db[dpt_name]
    url='http://www.pcoss.org/index.php?m=team'
    Field=[]
    Title=[]
    

    root='http://www.pcoss.org'
    r=requests.get(url)
    r.encoding='UTF-8'
    soup=bs(r.text,'lxml')
    td=soup.find('td',id='urlcll')
    for tr in td.find_all('table',width='100%')[1].find_all('tr',valign='bottom'):
        name=tr.find_all('td')[0].get_text(strip=True).replace(' ','').replace('\xa0','')
        url=root+tr.find_all('td')[0].a.attrs['href']
        title=tr.find_all('td')[1].get_text(strip=True).replace(' ','').replace('\xa0','')+'院士'
        print(name,url,title)
        item={'name':name,
                          'title':title,
                          'url':url,
                          #'field':Field[k]
                  }
        col.update({'url':item['url']},item,True)
    for table in td.find_all('table',width='100%')[3].find_all('table',width='95%'):
        field=table.tr.get_text(strip=True).replace(' ','').replace('\xa0','')
        for tr in table.find_all('tr',valign='bottom'):
            name=tr.find_all('td')[0].get_text(strip=True).replace(' ','').replace('\xa0','')
            url=root+tr.find_all('td')[0].a.attrs['href']
            title=tr.find_all('td')[1].get_text(strip=True).replace(' ','').replace('\xa0','')
            print(name,url,title,field)
            item={'name':name,
                          'title':title,
                          'url':url,
                          'field':field
                  }
            col.update({'url':item['url']},item,True)
def AEE_yanfa():
    dpt_name='醇醚酯化工清洁生产国家工程实验室_teachers'
    col=db[dpt_name]
    url='http://nel.xmu.edu.cn/14784/list.htm'
    Field=[]
    Title=[]
    

    root='http://chembio.xmu.edu.cn/'
    r=requests.get(url)
    r.encoding='UTF-8'
    soup=bs(r.text,'lxml')
    div=soup.find('div',id='wp_content_w6_0')
    for p in div.find_all('p')[:7]:
        title='教授'
        name=p.get_text(strip=True).replace(' ','').replace('\xa0','')
        if p.a:
            url=p.a.attrs['href']
            print(name,url,title)
            item={'name':name,
                          'title':title,
                          'url':url,
                          'field':'研发部'
                  }
            col.update({'url':item['url']},item,True)
    for p in div.find_all('p')[10:11]:
        title='副教授'
        name=p.get_text(strip=True).replace(' ','').replace('\xa0','')
        if p.a:
            url=p.a.attrs['href']
            print(name,url,title)
            item={'name':name,
                          'title':title,
                          'url':url,
                          'field':'研发部'
                  }
            col.update({'url':item['url']},item,True)        
    for p in div.find_all('p')[14:24]:
        title='副教授'
        name=p.get_text(strip=True).replace(' ','').replace('\xa0','')
        if p.a:
            url=p.a.attrs['href']
            print(name,url,title)
            item={'name':name,
                          'title':title,
                          'url':url,
                         'field':'研发部'
                  }
            col.update({'url':item['url']},item,True)     
def AEE_jichu():
    dpt_name='醇醚酯化工清洁生产国家工程实验室_teachers'
    col=db[dpt_name]
    url='http://nel.xmu.edu.cn/15107/list.htm'
    Field=[]
    Title=['教授','副教授','助理教授','2011研究助手']
    

    root='http://chembio.xmu.edu.cn/'
    r=requests.get(url)
    r.encoding='UTF-8'
    soup=bs(r.text,'lxml')
    i=0
    for ul in soup.find('div',id='wp_content_w6_0').find_all('ul'):
        for li in ul.find_all('li'):
            name=li.get_text(strip=True).replace(' ','').replace('\xa0','')
            title=Title[i]
            if li.a:
                url=li.a.attrs['href']
                print(name,title,url)
                item={'name':name,
                          'title':title,
                          'url':url,
                         'field':'基础部'
                  }
                col.update({'url':item['url']},item,True)   
        i+=1

def ercet():
    dpt_name='电化学技术教育部工程研究中心_teachers'
    col=db[dpt_name]
    url='http://ec.xmu.edu.cn/2344/list.htm'
    Field=[]
    #Title=['教授','副教授','助理教授','2011研究助手']
    

    root='http://chembio.xmu.edu.cn/'
    r=requests.get(url)
    r.encoding='UTF-8'
    soup=bs(r.text,'lxml')
    table=soup.find('div',id='wp_content_w4_0').find('table',style=False)
    i=0
    for a in table.find_all('a'):
        if i <=1:
            name=a.get_text(strip=True).replace(' ','').replace('\xa0','')
            title='院士'

            url=a.attrs['href']
            print(name,title,url)
            item={'name':name,
                          'title':title,
                          'url':url,
                         #'field':'基础部'
                  }
            col.update({'url':item['url']},item,True)
            i+=1
        else:
            name=a.get_text(strip=True).replace(' ','').replace('\xa0','')
            title='教授'

            url=a.attrs['href']
            print(name,title,url)
            item={'name':name,
                          'title':title,
                          'url':url,
                         #'field':'基础部'
                  }
            col.update({'url':item['url']},item,True)
            i+=1            

def cbf():
    dpt_name='福建省化学生物学重点实验室_teachers'
    col=db[dpt_name]
    url='http://121.192.177.81:90/hxswx/about/?86.html'
    Field=[]
    #Title=['教授','副教授','助理教授','2011研究助手']
    

    root='http://chembio.xmu.edu.cn/'
    r=requests.get(url)
    r.encoding='UTF-8'
    soup=bs(r.text,'lxml')
    div=soup.find('div',class_='con')

    for a in div.find_all('a'):

        tn=a.get_text(strip=True).replace(' ','').replace('\xa0','')
        if re.search('副',tn):
            title='副教授'

            url=a.attrs['href']
            name=tn.replace('副教授','')
            print(name,title,url)
            item={'name':name,
                          'title':title,
                          'url':url,
                         #'field':'基础部'
                  }
            col.update({'url':item['url']},item,True)
        elif re.search('高级',tn):
            title='高级工程师'

            url=a.attrs['href']
            name=tn.replace('高级','').replace('工程','').replace('师','')
            print(name,title,url)
            item={'name':name,
                          'title':title,
                          'url':url,
                         #'field':'基础部'
                  }
            col.update({'url':item['url']},item,True)            
        elif (not re.search('高级',tn) and re.search('工程',tn)):
            title='高级工程师'

            url='http://121.192.177.81:90'+a.attrs['href']
            name=tn.replace('高级','').replace('工程','').replace('师','')
            print(name,title,url)
            item={'name':name,
                          'title':title,
                          'url':url,
                         #'field':'基础部'
                  }
            col.update({'url':item['url']},item,True)
        else:
            title='教授'

            url=a.attrs['href']
            name=tn.replace('教授','')
            print(name,title,url)
            item={'name':name,
                          'title':title,
                          'url':url,
                         #'field':'基础部'
                  }
            col.update({'url':item['url']},item,True)          
def tc():
    dpt_name='理论化学研究中心_teachers'
    col=db[dpt_name]
    url='http://ctc.xmu.edu.cn/member.html'


    r=requests.get(url)
    r.encoding='GB2312'
    soup=bs(r.text,'lxml')
    table=soup.find('td',width='638')
    #print(table)
    for a in table.find_all('a'):
        #print(a)
        name=a.get_text(strip=True).replace(' ','').replace('\xa0','')
        title='教授'
        url=a.attrs['href']
        print(name,title,url)
        item={'name':name,
                          'title':title,
                          'url':url,
                         #'field':'基础部'
                  }
        col.update({'url':item['url']},item,True)      
#parse_chem()
#parse_chembio()
#pcoss()
#AEE_jichu()
#ercet()
tc()
