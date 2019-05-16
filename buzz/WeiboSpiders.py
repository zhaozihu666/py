# coding=gbk
#实现微博个人账号及粉丝微博信息的爬取。
from urllib.parse import urlencode
import requests
from pyquery import PyQuery as pq
import json

base_url ='https://m.weibo.cn/api/container/getIndex?'
headers = {
    'Host':'m.weibo.cn',
    'Referer':'https://m.weibo.cn/u/2830678474',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3664.3 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}   
#----------------------------------------------------------------------
def get_page(page):
    params = {
    'type':'uid',
    'value':'2830678474',
    'containerid':'1076032830678474',
    'page':page
    }
    url = base_url + urlencode(params)
    try:
        response = requests.get(url,headers = headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print('Error',e.args)
        
    """"""

#----------------------------------------------------------------------
def parse_page(json):
    if json:
        items = json.get('data').get('cards')
        for item in items:
            if page == 1 :
                continue
            else:
                item = item.get('mblog')
                weibo = {}
                weibo['id'] = item.get('id')
                weibo['text'] = pq(item.get('text')).text()
                weibo['attitudes'] = item.get('attitudes_count')
                weibo['comments'] = item.get('comments_count')
                weibo['reposts'] = item.get('repost_count')
                yield weibo
            
    """"""

if __name__ == '__main__':
    for page in range(1, 11):
        json = get_page(page)
        results = parse_page(json)
        for result in enumerate(results):
            print(result)
            