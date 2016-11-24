# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from nitu.items import NituItem


class NipicSpider(scrapy.Spider):
    name = "nipic"
    allowed_domains = ["www.nipic.com"]
    start_urls = ['http://www.nipic.com/']

    #爬取3个栏目链接和栏目名字
    def parse(self, response):
        category_urls = response.xpath('//div[@class="fl nav-item-wrap"]/a/@href').extract()
        category_names = response.xpath('//div[@class="fl nav-item-wrap"]/a/@title').extract()

        for i in range(1, len(category_urls)-2):
            category_url = response.urljoin(category_urls[i])
            category_name = category_names[i]

            yield Request(category_url, callback=self.group)

    #爬取图组链接和图组名
    def group(self, response):
        item = NituItem()
        group_urls = response.xpath('//dd[@class="menu-item-list clearfix"]/a/@href').extract()
        group_names = response.xpath('//dd[@class="menu-item-list clearfix"]/a/text()').extract()

        for j in range(0,len(group_urls)):
            group_url = response.urljoin(group_urls[j])
            item['group_name'] = group_names[j]

            request = scrapy.Request(group_url, callback=self.imgurl)
            request.meta['item'] = item
            yield request

    #爬取图组所有页图片的详情页链接
    def imgurl(self, response):
        print('\nCrawling page' + "======================================== " + response.url)
        item = response.meta['item']

        url = response.xpath('//li[@class="works-box mb17 fl"]/a/@href').extract()
        for k in url:
            per_url = k

            request1 = scrapy.Request(per_url, callback=self.detail)
            request1.meta['item'] = item
            yield request1

        xpath = '//div[@class="common-page-box mt10 align-center"]/a[@title="下一页"]/@href'
        next_page = response.xpath(xpath).extract()
        if next_page:
            next_page_url = response.urljoin(next_page[0])

            request2 = scrapy.Request(next_page_url, callback=self.imgurl)
            request2.meta['item'] = item
            yield request2

    #爬取详情页的图片名和图片链接
    def detail(self, response):
        item = response.meta['item']
        pic_name = response.xpath('//div[@id="J_worksBigImg"]/img/@alt').extract_first()
        item["pic_name"] = pic_name + '_' + (response.url.split('/')[-1]).split('.')[0]
        item["pic_url"] = response.xpath('//div[@id="J_worksBigImg"]/img/@src').extract()

        yield item
