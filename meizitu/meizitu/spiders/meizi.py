# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from meizitu.items import MeizituItem


class MeiziSpider(scrapy.Spider):
    name = "meizi"
    allowed_domains = ["meizitu.com"]
    start_urls = ['http://meizitu.com/']

    #提取所有的分类链接，进入分类页
    def parse(self, response):
        item = MeizituItem()
        category_urls = response.xpath('//div[@class="tags"]/span/a/@href').extract()
        category_names = response.xpath('//div[@class="tags"]/span/a/@title').extract()

        for i in range(0, len(category_urls)):
            category_url = category_urls[i]
            item['category_name'] = category_names[i]

            request = scrapy.Request(category_url, callback=self.get_group)
            request.meta['item'] = item
            yield request

    #提取所有页中的图组链接，进入图组页
    def get_group(self, response):
        item = response.meta['item']
        group_urls = response.xpath('//ul[@class="wp-list clearfix"]//div/a/@href').extract()
        group_names = response.xpath('//ul[@class="wp-list clearfix"]//img/@alt').extract()

        for j in range(0, len(group_urls)):
            group_url = group_urls[j]
            item['group_name'] = group_names[j].replace('<b>', '').replace('</b>', '').replace(' ','')

            request1 = scrapy.Request(group_url, callback=self.get_img_url)
            request1.meta['item'] = item
            yield request1

        xpath = '//div[@id="wp_page_numbers"]//a[text()="下一页"]/@href'
        next_page = response.xpath(xpath).extract()
        if next_page:
            next_page_url = response.urljoin(next_page[0])

            request2 = scrapy.Request(next_page_url, callback=self.get_group)
            request2.meta['item'] = item
            yield request2

    #提取每张图片的链接
    def get_img_url(self, response):
        print("\nCrawling page" + "======================================== " + response.url)
        item = response.meta['item']

        item['img_urls'] = response.xpath('//div[@id="picture"]/p/img/@src').extract()
        item['img_names'] = response.xpath('//div[@id="picture"]/p/img/@alt').extract()

        yield item
