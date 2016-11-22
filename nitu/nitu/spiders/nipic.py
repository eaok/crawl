# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from nitu.items import NituItem


class NipicSpider(scrapy.Spider):
    name = "nipic"
    allowed_domains = ["www.nipic.com"]
    start_urls = ['http://www.nipic.com/']

#爬取栏目链接
    def parse(self, response):
        urldata = response.xpath("//div[@class='fl nav-item-wrap']/a/@href").extract()
        category_urls = urldata[1:4]

        for i in category_urls:
            category_url = response.urljoin(i)
            yield Request(url=category_url, callback=self.next)

#爬取图组链接
    def next(self, response):
        item = NituItem()
        category_names = response.xpath('//div[@class="menu-box-bd"]//strong/text()').extract()
        group_urls = response.xpath('//dd[@class="menu-item-list clearfix"]/a/@href').extract()
        group_names = response.xpath('//dd[@class="menu-item-list clearfix"]/a/text()').extract()

        for j in range(0,len(group_urls)):
            group_url = response.urljoin(group_urls[j])
            item['group_name'] = group_names[j]
#            print(category_url)
            request = scrapy.Request(url=group_url, callback=self.next2)
            request.meta['item'] = item
            yield request


#进入每页的链接
    def next2(self, response):
        print('\nCrawling page' + "======================================== " + response.url)
        item = response.meta['item']

        url = response.xpath('//li[@class="works-box mb17 fl"]/a/@href').extract()
        for k in url:
            per_url = k
            request1 = scrapy.Request(per_url,callback=self.next3)
            request1.meta['item'] = item
            yield request1

        xpath = '//div[@class="common-page-box mt10 align-center"]/a[@title="下一页"]/@href'
        next_page = response.xpath(xpath).extract()

        if next_page:
#            print(next_page[0] + '====================================================')
            next_page_url = response.urljoin(next_page[0])
#            print(next_page_url)
            request2 = scrapy.Request(url=next_page_url, callback=self.next2)
            request2.meta['item'] = item
            yield request2

    def next3(self, response):
        print('Crawling page' + "======================================== " + response.url)
        item = response.meta['item']
        pic_name = response.xpath('//div[@id="J_worksBigImg"]/img/@alt').extract_first()
        item["pic_name"] = pic_name + '_' + (response.url.split('/')[-1]).split('.')[0]
#        item["pic_name"] = pic_name + '_' + re.findall('show/(.*?).html', response.url)[0]
        item["pic_urls"] = response.xpath('//div[@id="J_worksBigImg"]/img/@src').extract()
#        print(item)
        yield item
