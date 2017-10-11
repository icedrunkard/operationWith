import requests
from bs4 import BeautifulSoup as bs

url='http://cache.baiducontent.com/c?m=9d78d513d9d430a84f9e95690c66c0171c43f7652ba6d30209de8448e2732a42501192ac26520772d2d20f6715e80902e5aa7034751421c486d5d916cabbe57674d47e632647da5612a448f2945b7e9d3d872deeb81391ad804684d9d9c4d42544c157127af6e7fc5f171ec178fb6426e3d0c94b11591bbfe635&p=ce6dc54ad5c14be01aa98e2d0214cd&newp=8a769a4792d202ec08e2977c074e8e231615d70e3cd2d2126b82c825d7331b001c3bbfb423241104d9c27b620aa54b56eef13279370923a3dda5c91d9fb4c57479cc367733&user=baidu&fm=sc&query=%C5%A3%C7%E4%C1%D8+%C1%EC%D3%A2&qid=f06052730002ca41&p1=1'

r=requests.get(url)
print(r.encoding)
print(type(r))
soup=bs(r.text,'lxml')
link=soup.find('base').attrs['href']
print(link,'===>',type(link))
r.encoding='utf-8'
print(r.encoding)
soup=bs(r.text,'lxml')
link=soup.find('base').attrs['href']
print(link,'===>',type(link))
