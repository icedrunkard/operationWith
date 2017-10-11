# -*- coding: utf-8 -*-
from urllib.parse import quote_plus
import requests
from qText import query



def genHeaders(name,school):
    H=[]

    headers={

    'authorization':'Basic aWNlZDpydW5r',
    'cookie':'UM_distinctid=15daa2678875e7-02da00b929ef17-314b7b5f-1fa400-15daa26788870a; CNZZDATA1260920938=357490342-1501793144-%7C1501793144',
    'referer':'https://vip.kuaimen.bid/',
    'upgrade-insecure-requests':'1',
    'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.2372.400 QQBrowser/9.5.10548.400',
    }



    H.append(headers)
    return H

genHeaders('王祥','中南大学')
