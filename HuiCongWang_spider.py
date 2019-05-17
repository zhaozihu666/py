# 用来提取慧聪网指定关键词公司名称及其联系方式。
# 根据关键字获取公司列表，迭代就行
# 进入公司页面获取联系方式。


import requests
from lxml import etree

def get_company_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3664.3 Safari/537.36'
        }
    response = requests.get(url,headers=headers)
    if response.status_code ==200:
        print("此页爬取成功")
    html = response.text
    selector = etree.HTML(html)
    company_info = {}
    company_name = selector.xpath('//dt[@class="til"]///h3/a[1]/text()')
    company_url = selector.xpath('//dt[@class="til"]//h3/a[1]/@href')
    company_info[company_name] = company_url
    return company_info


# def parse_company(url):
# # 提取公司联系人姓名和联系方式
#     respone = requests.get(url)
#     rep = etree.HTML(respone)
#     comapany_p_name = rep.xpath('//div[@class="leftBoxCon ContactBox"]/ul/li[1]')# 进一步选择
#     comapany_p_num = rep.xpath('//div[@class="leftBoxCon ContactBox"]/ul/li[3]')# 进一步选择
#     return comapany_p_name,comapany_p_num


# def next_page(url,page):
#     """获取下一页内容"""
#     next_url = url + "&pnum" + str(page)
#      return next


if __name__ == '__main__':
    # print('请输入要查找的网站：(例如http:\\www.baidu.com)')
    url = "https://s.hc360.com"
    # print('请输入要查重的公司类型：（例如 塑业）')
    kw = "塑业"
    url = url + "/company/search.html?kwd=" + kw
    company_info = get_company_url(url)
    # for page in range(2,50):
    #     next_page(url,page)

    print("爬取完成")
    print(company_info)
