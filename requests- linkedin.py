import requests
from bs4 import BeautifulSoup as bs

url='https://cn.linkedin.com/in/%E5%8D%BF%E9%9C%96-%E7%89%9B-b1649797'


headers={


'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, sdch',
'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'DNT':'1',
'Host':'cn.linkedin.com',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36',
    }








s=requests.session()






r=s.get(url,headers=headers)
print(r.text)


