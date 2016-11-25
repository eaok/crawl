# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from wallpaper.items import WallpaperItem

class IvskySpider(scrapy.Spider):
    name = "ivsky"
    allowed_domains = ["ivsky.com"]
    start_urls = ['http://ivsky.com/bizhi/1920x1080/']

    #提取所有的分类链接，进入分类页
    def parse(self, response):
        item = WallpaperItem()
        category_urls = response.xpath("//ul[@class='bzmenu']/li[position()>1]/a/@href").extract()
        category_names = response.xpath("//ul[@class='bzmenu']/li[position()>1]/a/text()").extract()
#        print(category_urls)
#        print(category_names)

        for i in range(0, len(category_urls)):
            category_url = "http://www.ivsky.com" + category_urls[i]
            item["category_name"] = category_names[i]
#            print(category_url)
#            print(category_name)
            request = scrapy.Request(category_url, callback=self.get_group)
            request.meta['item'] = item
            yield request

    #提取所有图组页链接，并进入图组页
    def get_group(self, response):
        print("\nCrawling page" + "\t@@@@@@@@@@@@@@@@@@@@\t" + response.url)
        item = response.meta['item']

        group_urls = response.xpath("//ul[@class='ali']/li/div/a/@href").extract()
        group_names = response.xpath("//ul[@class='ali']/li/div/a/@title").extract()
        for j in range(0, len(group_urls)):
            group_url = response.urljoin(group_urls[j])
            item['group_name'] = group_names[j]

            request1 = scrapy.Request(group_url, callback=self.get_img_url)
            request1.meta['item'] = item
            yield request1

        xpath = '//div[@class="pagelist"]/a[@class="page-next"]/@href'
        next_page = response.xpath(xpath).extract()
        if next_page:
            next_page_url = response.urljoin(next_page[0])

            request2 = scrapy.Request(next_page_url, callback=self.get_group)
            request2.meta['item'] = item
            yield request2


    #提取图组所有的缩略图的链接,返回给item
    def get_img_url(self, response):
        print("\nCrawling page" + "\t====================\t" + response.url)
        item = response.meta['item']

        item["img_urls"] = response.xpath("//ul[@class='pli']/li/div/a/img/@src").extract()
#        print(item)
        yield item

        next_page = response.xpath("//div[@class='pagelist']/a[@class='page-next']/@href").extract()
        if next_page:
            next_page_url = response.urljoin(next_page[0])

            request3 = scrapy.Request(next_page_url, callback=self.get_img_url)
            request3.meta['item'] = item
            yield request3

