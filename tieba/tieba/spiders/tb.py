# -*- coding: utf-8 -*-
import scrapy


class TbSpider(scrapy.Spider):
    name = 'tb'
    allowed_domains = ['tieba.baidu.com']
    start_urls = ['https://tieba.baidu.com/f?ie=utf-8&kw=%E6%9D%8E%E6%AF%85%E5%90%A7&fr=search&pn=0&']
    def parse(self, response):
        #提取列表页
        div_list = response.xpath("//*[@id='thread_list']/li[21]/div/div[2]/div[1]/div[1]")
        for div in div_list:
            item = {}
            item['href'] = div.xpath('./a/@href').extract_first()
            item['title'] = div.xpath('./a/text()').extract_first()
            item["img_list"] = []
            if item["href"] is not None:
                item["href"] = "https://tieba.baidu.com/" + item["href"]
                yield scrapy.Request(
                    item["href"],
                    callback=self.parse_detail,
                    meta= {"item":item}
                )
            #翻页
            next_url = response.xpath("//a[text()='下一页']/@href").extract_first()
            if next_url is not None:
                next_url = "https://tieba.baidu.com/" + next_url
                yield scrapy.Request(
                    next_url,
                    callback=self.parse()
                )

    def parse_detail(self,response):
        #提取详情页
        item = response.meta["item"]

        item["img_list"].extend(response.xpath("//img[@class='BDE_Image']/@src").extract())
        next_url = response.xpath("//a[text()='下一页']/@href").extract_first()
        if next_url is not None:
            next_url = "https://tieba.baidu.com/" + next_url
            yield scrapy.Request(
                next_url,
                callback=self.parse_detail(),
                meta={"item":item}
            )
        else:
            print(item)

