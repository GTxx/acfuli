#! /usr/bin/env python
#encoding:utf-8

import requests
from bs4 import BeautifulSoup
import json, os
import re, urllib
import time, threading

lock = threading.Lock()

acUrlfirst = 'http://search.acfun.tv/search?cd=1&type=2&q=%E7%A6%8F%E5%88%A9&sortType=-1&field=title&parentChannelId=63&sortField=releaseDate&pageNo='
acUrlend = '&pageSize=10&aiCount=3&spCount=3&isWeb=1&sys_name=pc'

headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'}
titleList=[]
urlList=[]
notfulire = r'.*?(谷歌|中秋|汪星人|央企|阿迪王|贫民窟|小说|腐女|干部|腐|求助|官方|政府|失眠|动物|福利院|养老|教育部).*?'

def getPageNum():
    sumItem = 180
    acUrl = acUrlfirst + '1' + acUrlend
    try:
        mainRes = requests.get(acUrl,timeout=None)
        jsonRes = json.loads(mainRes.content.split('system.tv=')[1])
        sumItem = jsonRes['data']['page']['totalCount']
    except:
        pass
    pageNum = sumItem/10
    return pageNum

def getImagesByUrl(url,title):
    folder = url.split('/').pop()
    os.mkdir(title)
    fuliRes = requests.get(url,headers=headers,timeout=None)
    fuliimgtag = BeautifulSoup(fuliRes.content).find(id='area-player').find_all('img')
    for item in fuliimgtag:
        if item['src'].split('.').pop() != 'gif':
            urllib.urlretrieve(item['src'], title+'/'+item['src'].split('/').pop())
            print item['src']

def loop(n):
    print 'thread %s is running...' % threading.current_thread().name
    acUrl = acUrlfirst + str(n) + acUrlend
    try:
        mainRes = requests.get(acUrl,headers=headers,timeout=None)
        jsonRes = json.loads(mainRes.content.split('system.tv=')[1])
        datalist = jsonRes['data']['page']['list']
        for item in datalist:
            if item:
                if item['title'].encode('utf-8').find('福利') != -1 and not re.match(notfulire,item['title'].encode('utf-8')):
                    titleList.append(item['title'] +' : ' + item['contentId'])
                    print item['title'] +' : ' + item['contentId']
                    fuliUrl = 'http://www.acfun.tv/a/'+item['contentId']
                    getImagesByUrl(fuliUrl,item['title']+item['contentId'])
    except:
        print 'timeout'

n = getPageNum()

threads = []
for i in range(n):
    threads.append(threading.Thread(target=loop, args=(i+1,),name=str(i)))

for t in threads:
    t.start()

for t in threads:
    t.join()
