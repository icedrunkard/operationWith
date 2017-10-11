# -*- coding: utf8 -*-

# 已爬取成功
import pymongo
import requests
import bs4
from bs4 import BeautifulSoup as bs
import re
client = pymongo.MongoClient('localhost:27009')
db = client['THU']
def trans(title0):
    title=[]
    if 'Y' in title0:
        title.append('院士')
    if 'Q' in title0:
        title.append('国家千人计划教授')
    if 'C' in title0:
        title.append('长江特聘教授')
    if 'J' in title0:
        title.append('杰出青年基金获得者')
    if len(title)>0:

        return title
    else:
        return None
def has_sup(each):
    for s in each.next_siblings:

        if type(s)==bs4.element.NavigableString:

            continue
        elif s.name=='a':

            return False
        elif s.sup:
            return s.sup.get_text(strip=True)
            #return [s.find_all('sup')[i].get_text(strip=True) for i in range(0,len(s.find_all('sup')))]
        else:

            continue        

    else:
        return False
def parse_chemeng():
    dpt_name='化学工程系_teachers'
    col=db[dpt_name]
    
    index='http://www.chemeng.tsinghua.edu.cn/podcast.do?method=staff&cid=3'
    root='http://www.chemeng.tsinghua.edu.cn/'
    TITLE=['两院院士','双聘/兼职/讲座教授','正高级','副高/中级','退休教职工']
    r=requests.get(index)
    r.encoding='UTF-8'
    soup=bs(r.text,'lxml')
    i=0
    for t in soup.find_all('table',class_="teachName"):
        
        if t.find('td'):
            for td in t.find_all('td'):
                name=td.get_text(strip=True).replace('\u3000','')#去除空格
                title=TITLE[i]
                url=root+td.a.attrs['href']
                print(name,title,url)
                item={'name':name,
                      'title':title,
                      'url':url,
                    }
                #col.insert(item)#已完成
            i+=1


def parse_chem():
    dpt_name='化学系_teachers'
    col=db[dpt_name]
    
    index='http://www.chem.tsinghua.edu.cn/publish/chem/7167/index.html'
    root='http://www.chem.tsinghua.edu.cn'
    FIELD=[]
    NAME=set()
    r=requests.get(index)
    r.encoding='UTF-8'
    soup=bs(r.text,'lxml')

    for t in soup.find_all('p',style="TEXT-ALIGN: left"):#每个专业的开头
        FIELD.append(t.get_text(strip=True))
        S=[]
        for s in t.next_siblings:
            if not str(s).startswith('<p style="TEXT-ALIGN: left">'): #如果不是专业开头              
                if str(s).startswith('<p style="TEXT-ALIGN: left; MARGIN-LEFT: 40px">'):#就是人名行开头
                    for each in s.find_all('a'):#只选取有主页链接的老师

                        item={}
                        name=each.get_text(strip=True).replace('\xa0','').replace(' ','')

                        NAME.add(name)
                        print(name)
                        item['name']=name
                        
                        if each.attrs['href'].startswith('http'):
                            url=each.attrs['href']
                            item['url']=url
                        else:
                            url=root+each.attrs['href']
                            item['url']=url

                        if has_sup(each):
                            title0=has_sup(each)
                            title=trans(title0)
                            item['title']=title
                            print(title0,title)


                        field=t.get_text(strip=True)

                        item['field']=field
                        col.insert(item)


                        print('==================================================')

                else:#next_siblings中的空白
                    continue
            else:                
                break

    print(FIELD)


#parse_chemeng()

parse_chem()
