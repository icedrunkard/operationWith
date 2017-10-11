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
proxies ={"http"  : proxyMeta,"https" : proxyMeta,}
url ='http://cn.linkedin.com/in/%E5%8D%BF%E9%9C%96-%E7%89%9B-b1649797'
headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
for i in range(20):
    r=requests.get(url)
    print(r.status_code)
