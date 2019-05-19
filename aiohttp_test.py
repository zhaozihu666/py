import aiohttp
import asyncio
import aiomysql
from lxml import etree

stoping = False
start_url = "https://s.hc360.com/company/search.html?kwd=精密模具"
# 等待爬取列
waitting_urls = [f"https://s.hc360.com/company/search.html?kwd=精密模具&pnum={num}" for num in range(2, 20)]
# set去重
seen_urls = set()
# header = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
# }
async def fetch(url, session):
        try:
            async with session.get(url) as resp:
                if resp.status in [200, 201]:
                    print("{}请求成功".format(url))
                    data = await resp.text()
                    return data
        except Exception as e:
            print(e)

def extract_urls(html):
    urls = []
    selector = etree.HTML(html)
    urls_items = selector.xpath('//dt[@class="til"]//h3/a[1]/@href')
    for url in urls_items:
        if url and url not in seen_urls:
            urls.append(url)
            waitting_urls.append(url)
    return urls

async def init_urls(url, session):
    html = await fetch(url, session)
    seen_urls.add(url)
    extract_urls(html)

async def fetch_num(url, session, pool):
    # fatch_num
    html = await fetch(url, session)
    selector = etree.HTML(html)
    try:
        CompanyName = selector.xpath('//a[@id="companyName"]/text()')[0]
        CompanyNum = selector.xpath('//span[contains(text(),"手机")]/following-sibling::span/text()')[0]
    except Exception as e:
        CompanyName = ""
        CompanyNum = ""
        print(e,"提取失败")
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT 10")
            insert_sql = "insert into company_info(company_name,company_num) values('{}','{}')".format(CompanyName,CompanyNum)
            await cur.execute(insert_sql)

async def consumer(pool):
    async with aiohttp.ClientSession() as session:
        while not stoping:
            if len(waitting_urls) == 0:
                await asyncio.sleep(0.5)
                continue
            url = waitting_urls.pop()
            if len(url) > 50:
                asyncio.ensure_future(init_urls(url, session))
            else:
                asyncio.ensure_future(fetch_num(url, session, pool))



async def main(loop):
    pool = await aiomysql.create_pool(host='127.0.0.1', port=3306,
                                           user='root', password='zgh19970701',
                                           db='aiomysql_test', loop=loop,
                                           charset="utf8", autocommit=True)
    async with aiohttp.ClientSession() as session:
        html = await fetch(start_url, session)
        seen_urls.add(start_url)
        extract_urls(html)
    asyncio.ensure_future(consumer(pool))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(main(loop))
    loop.run_forever()
