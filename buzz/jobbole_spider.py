#coding=gbk
import time
from tornado import ioloop, httpclient, gen
from lxml import etree
import requests

Start = 'https://s.hc360.com/company/search.html?kwd=塑业'

count = 0 #统计爬取了几个文章
#----------------------------------------------------------------------
async def parse_archive(url):
    # 获取页面内容
    # resp = requests.get(url)
    # html = resp.text
    resp = await httpclient.AsyncHTTPClient().fetch(url)
    html = resp.body.decode()
    selector = etree.HTML(html)
    CompanyName = selector.xpath('//a[@id="companyName"]')
    CompanyNum = selector.xpath('//div[@class="leftBoxCon ContactBox"]/ul/li[3]')
    return CompanyName,CompanyNum

    
async def fetch_list(url=Start):
    global count
    # 获取页面内容
    resp = await httpclient.AsyncHTTPClient().fetch(url)
    html = resp.body.decode()
    selector = etree.HTML(html)
    # nodes = selector.xpath('//div[@class="post-meta"]//a[@class="archive-title"]')
    urls = selector.xpath('//dt[@class="til"]//h3/a[1]/@href')
    for url in urls:
        print(parse_archive(url))
        count += 1
        print(count)

    # 处理下一页
    if url == Start:
        # max_num = selector.xpath('//div[contains(@class,"navigation")]/a[contains(@class,"page-numbers")]')[-2]
        # max_num = int(max_num.text)
        # tasks = [fetch_list(f"http://python.jobbole.com/all-posts/page/{num}") for num in range(2, max_num+1)]
        tasks = [fetch_list(f"https://s.hc360.com/company/search.html?kwd=塑业&pnum={num}") for num in range(2, 50)]
        await gen.multi(tasks)



time1 = time.time()      
loop = ioloop.IOLoop.current()
loop.run_sync(fetch_list)
time2 = time.time()

print(f"time:{time2-time1}")


    
    
        
        