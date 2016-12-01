# -*- coding: utf-8 -*-
import scrapy
import re
import urllib.request
from taobao.items import TaobaoItem

class TbSpider(scrapy.Spider):
    name = "tb"
    allowed_domains = ["tabao.com"]
    start_urls = ['http://tabao.com/']

    def parse(self, response):
        key = "硬盘"
        for i in range(0, 101):
            url="https://s.taobao.com/search?q=" + str(key) + "&s=" + str(44*i)
            yield scrapy.Request(url, callback=self.page, dont_filter=True)

    def page(self, response):
        body = response.body.decode("utf-8", "ignore")
        patid = '"nid":"(.*?)"'
        allid = re.compile(patid).findall(body)

        for j in range(0,len(allid)):
            thisid = allid[j]
            url1 = "https://item.taobao.com/item.htm?id=" + str(thisid)
            yield scrapy.Request(url1, callback=self.next, dont_filter=True)

    def next(self, response):
        item = TaobaoItem()
        item["title"]=response.xpath('//meta[@name="keywords"]/@content').extract()
        item["link"]=response.url
        item["price"]=response.xpath("//em[@class='tb-rmb-num']/text() | //div/span[@class='tm-price']/text()").extract()

        patid = 'id=(.*?)$'
        thisid = re.compile(patid).findall(response.url)[0]

        commenturl = "https://rate.taobao.com/detailCount.do?callback=jsonp100&itemId=" + str(thisid)
        commentdata = urllib.request.urlopen(commenturl).read().decode("utf-8","ignore")
        pat='"count":(.*?)}'
        item["comment"] = re.compile(pat).findall(commentdata)

        #print(item)
        yield item

