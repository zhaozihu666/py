#coding=gbk
from newspaper import Article
import jieba.analyse
import requests
import time


url = 'http://www.chinaz.com/news/2018/1227/975966.shtml'
news = Article(url, language='zh')
time2 = time.time()
news.download()
print(type(news))
time3 = time.time()
news.parse()
time4 = time.time()
title = news.title
tags = news.tags
text = news.title
print("获取完成")

print(f"time1:{time3-time2}")
print(f"time2:{time4-time3}")

