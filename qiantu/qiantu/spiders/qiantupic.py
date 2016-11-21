# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from qiantu.items import QiantuItem

class QiantupicSpider(scrapy.Spider):
    name = "qiantupic"
    allowed_domains = ["www.58pic.com"]
    start_urls = ['http://www.58pic.com/']

#第一层循环为提取所有的分类链接
    def parse(self, response):
        urldata=response.xpath("//div[@class='moren-content']/a/@href").extract()

        for i in range(0,len(urldata)):
            thisurldata=urldata[i]
            yield Request(url=thisurldata,callback=self.next)

#第二层循环为提取分类页面下的页面链接
    def next(self, response):
        thisurl = response.url
        pagelist = response.xpath("//div[@id='showpage']/a/text()").extract()

        if(len(pagelist)>=2):
            page = pagelist[-2]                   #pagelist[-1]为下一页

            for j in range(1,int(page) + 1):      #j从1开始的，所以要加1
                pageurl = thisurl+"id-"+str(j) + ".html"
                yield Request(url = pageurl, callback = self.next2)
        else:
            pass

#返回每页中的图片链接
    def next2(self, response):
        print("\nCrawling page" + "======================================== " + response.url)

        item = QiantuItem()
        item["url"] = response.xpath("//a[@class='thumb-box']/img[not(@class)]/@src | //a[@class='thumb-box']/img/@src1").extract()
        item["folder_name"] = response.url.split('/')[3]

        yield item

