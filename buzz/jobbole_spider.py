#coding=gbk
import time
from tornado import ioloop,httpclient, gen 
import requests
from lxml import etree

Start = 'http://python.jobbole.com/all-posts/'

count = 0 #ͳ����ȡ�˼�������
#----------------------------------------------------------------------
def get_archive(node):
    """��a��ǩ�л�ȡ��������"""
    title = node.text
    url = node.attrib['href']
    return title,url
    
async def fetch_list(url=Start):
    global count
    #��ȡҳ������
    resp = await httpclient.AsyncHTTPClient().fetch(url)
    html = resp.body.decode()
    selector = etree.HTML(html)
    nodes = selector.xpath('//div[@class="post-meta"]//a[@class="archive-title"]')
    for node in nodes:
        print(get_archive(node))
        count += 1
        print(count)
        
    #������һҳ
    if url ==Start:
        max_num = selector.xpath('//div[contains(@class,"navigation")]/a[contains(@class,"page-numbers")]')[-2]
        max_num = int(max_num.text)
        tasks = [ fetch_list(f"http://python.jobbole.com/all-posts/page/{num}") for num in range(2,max_num+1)]
        await gen.multi(tasks)

time1 = time.time()      
loop = ioloop.IOLoop.current()
loop.run_sync(fetch_list)
time2 = time.time()

print(f"time:{time2-time1}")


    
    
        
        