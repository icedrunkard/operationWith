import requests


proxyHost = "proxy.abuyun.com"
proxyPort = "9020"


proxyUser = "H264P9E9M949159D"#"H7394I09T0C1L82P" 
proxyPass = "1C6AED9CB122390C"#"427F77676DBAFF9F" 
proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
                      "host" : proxyHost,
                      "port" : proxyPort,
                      "user" : proxyUser,
                      "pass" : proxyPass,
                        }
proxiesA ={"http"  : proxyMeta,"https" : proxyMeta,}

cookies='join_wall=v=2&AQEnYcDYZ_pWtgAAAV1AxYWnahKrmAXzkx2V8oaX-XKHWHjvC7UpEZIus6-gDBUeYRSTDP-lJ1Wa-aEU3WagMR8pyXK9gInf-_lzHGc8u9H-YNIp9zlKaNF87Ewwtai9ld8KcADUOSWp07LiWgct; Max-Age=86400; Expires=Sat, 15 Jul 2017 11:04:33 GMT; Path=/; Domain=linkedin.com; Secure; HTTPOnly'


url ='https://cn.linkedin.com/in/%E5%8D%BF%E9%9C%96-%E7%89%9B-b1649797'
headers0={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
         'Referer':'http://cache.baiducontent.com/c?m=9d78d513d9d430a84f9e95690c66c0171c43f7652ba6d30209de8449e3732a42501192ac26520772d2d20f6715e80902e5aa7034751421c486d5d916cabbe57674d47e632647da5612a448f2945b7e9d3d872deeb81391ad804684d9d9c4d42544c157127af6e7fc5f171ec178fb6426e3d0c94b11591bbfe635&p=8e769a478f934eaf58ebcc3a7f4f8a&newp=8f718616d9c11aff57ed947858508c231610db2151d6d1126b82c825d7331b001c3bbfb423241606d7c0786d0aad4e56eefb3476330327a3dda5c91d9fb4c57479d3&user=baidu&fm=sc&query=%C5%A3%C7%E4%C1%D8%C1%EC%D3%A2&qid=c6313f6c0037d5cd&p1=1',
         }
params={'csrfToken':'jax:6522694436539678614'}







for i in range(20):
    r=requests.get(url,headers=headers0,proxies=proxiesA)
    print(r.status_code,'-'*20)
    #print(r.headers)
