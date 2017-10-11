#-*-coding:utf8-*-
import time
from urllib.parse import urlencode
import pymongo
import requests

"""期刊CJFQ/特色期刊CJFN/博士CDFD/硕士CMFD/
国内会议CPFD/专利SCOD/国际会议IPFD/学术辑刊CCJD/
标准CISD/成果SNAD/报纸CCND/年鉴CYFD"""

url_root='http://kns.cnki.net/kns/request/SearchHandler.ashx?'

def paramize(teacher,school):
    expertvalue="发表时间 between ('2010-01-01','') and ((作者={0} or 中英文作者={0} or 作者名称={0}) and (机构%'{1}' or 单位%'{1}' or 作者单位%'{1}' or 学位授予单位%'{1}'))".format(teacher,school)
    times = time.strftime('%a %b %d %Y %H:%M:%S') + ' GMT+0800 (中国标准时间)'

    params = {    
        'action':'',
        'NaviCode':'*',
        'ua': '1.21',
        'PageName': 'ASP.brief_result_aspx',
        'DbPrefix': 'SCDB',
        'DbCatalog':'中国学术文献网络出版总库',
        'ConfigFile': 'SCDB.xml',
        'db_opt': 'CJFQ,CJFN,CDFD,CMFD,CPFD,IPFD,CCJD',#
        'expertvalue': expertvalue,
        'his': '0',
        '__': times
            }
    
    url_params=urlencode(params)
    url_SearchHandler=url_root+url_params
    def req():
        s=requests.Session()
        s.get(url_SearchHandler)
        url_brief='http://kns.cnki.net/kns/brief/brief.aspx?pagename=ASP.brief_result_aspx&dbPrefix=SCDB&dbCatalog=%e4%b8%ad%e5%9b%bd%e5%ad%a6%e6%9c%af%e6%96%87%e7%8c%ae%e7%bd%91%e7%bb%9c%e5%87%ba%e7%89%88%e6%80%bb%e5%ba%93&ConfigFile=SCDB.xml&research=off&keyValue=&S=1&recordsperpage=50'
        r=s.get(url_brief)
        print(r.text)
    return req()

paramize(teacher='朱静',school='清华大学')
raw=input('请按任意键结束：')

