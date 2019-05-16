#coding=gbk
from lxml import etree
import requests
from tornado import ioloop,httpclient, gen
from requests.exceptions import RequestException
import time 
import json
#优化，分为两个内容，第一个抓取url，从入口开始抓取到最初页面的所有文章url，（还要实现增量抓取功能）
#第二个模块，根据url对文章内容进行提取，分析。
#第三个模块，将文章内容保存到数据库中。
#----------------------------------------------------------------------
def get_page_url(primary_url):
    """批量获取url"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3710.0 Safari/537.36'
        }
        response = requests.get(primary_url,headers = headers)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            doc = etree.HTML(response.text)
            url_list = doc.xpath('//div[@id="tagcontentlist"]//h4/a/@href')
            print(len(url_list))
            return url_list
        return None
    except RequestException:
        return None    
    
#----------------------------------------------------------------------
def get_one_page(url):
    """获取页面源码"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3710.0 Safari/537.36'
        }
        response = requests.get(url,headers = headers)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            return response.text
        return print('访问失败')
    except RequestException:
        return None
    
#----------------------------------------------------------------------
def parse_page(html):
    """提取所需内容"""
    doc = etree.HTML(html)
    title = doc.xpath('//title/text()')
    keywords = doc.xpath('//meta[@name="keywords"]/@content')
    description = doc.xpath('//meta[@name="description"]/@content')
    summ = doc.xpath('//div[@id="ctrlfscont"]/p/text()')
    my_summary = ''
    for item in summ:
        my_summary += item   
    result = {
        'title': title[0],
        'keywords':keywords[0],
        'desceription':description[0],
        'summary':my_summary
    }
    return result
#----------------------------------------------------------------------
def write_to_file(content):
    """保存文件或者保存至数据库"""
    with open('result.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
    #----------------------------------------------------------------------
def main():
    """调用函数"""
    tasks = [get_page_url(f'http://www.chinaz.com/news/{num}.shtml' for num in range(2,30))]
    await gen.multi(tasks)
    for url in tasks:
        url = "http:"+url
        html = get_one_page(url)
        result = parse_page(html)
        write_to_file(result)
            
if __name__ == '__main__':
    main()
    ioloop.IOLoop.current()
    loop.run_sync(get_page_url)
    time.sleep(3)
