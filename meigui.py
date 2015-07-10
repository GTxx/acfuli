#!/usr/bin/env python
#encoding:utf-8

import requests, json, re
import time, threading
import os, urllib
from bs4 import BeautifulSoup

#获取总页数
def getPageNum(url):
    url = url.format('1')
    res = json.loads(requests.get(url).content)
    return res['page']['totalPage']

#下载每篇文章图片
def getImagesByUrl(url,title):
    os.mkdir(title)
    fuliRes = requests.get(url,timeout=None)
    fuliimgtag = BeautifulSoup(fuliRes.content).find(id='area-player').find_all('img')
    for item in fuliimgtag:
        if item['src'].split('.').pop() != 'gif':   #去除ac娘表情，TODO
            urllib.urlretrieve(item['src'], title+'/'+item['src'].split('/').pop())
            print item['src']

#匹配文章
def loop(url):
    print 'thread ' + url
    matches = r'.*?(玫瑰深夜剧场|福利).*?'

    try:
        res = json.loads(requests.get(url,timeout=None).content)['contents']
        for item in res:
            if re.match(matches, item['title'].encode('utf-8')):
                print item['title']
                prefix = 'http://www.acfun.tv'
                getImagesByUrl(prefix+item['url'], item['title'])
    except:
       print 'fail'

#入口
def getFuli(url):
    firstPage = url.format(1)
    totalPage = getPageNum(firstPage)

    threads = []
    for i in range(1, totalPage):
        fuli = url.format(i)
        threads.append(threading.Thread(target=loop, args=(fuli,),name=fuli))

    for t in threads:
        t.start()

    for t in threads:
        t.join()

#魔宫玫瑰
url = 'http://www.acfun.tv/u/contributeList.aspx?userId=454711&pageSize=10&pageNo={}&channelId=0'
getFuli(url)
