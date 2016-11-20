# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from meizitu.items import MeizituItem

global category_name

class MeiziSpider(scrapy.Spider):
    name = "meizi"
    allowed_domains = ["meizitu.com"]
    start_urls = ['http://meizitu.com/']

#提取所有的分类链接，进入分类页
    def parse(self, response):
        category_list = response.xpath("//div[@class='tags']/span/a/@href").extract()
        category_list = list(set(category_list))
        category_list.sort()

        for i in range(0, len(category_list)):
            category_url = category_list[i]
            category_name = category_url.split('/')[-1].split('.')[0]
#            print(category_url)
#            print(category_name)
            yield Request(url = category_url, callback = self.get_page)

#提取页数链接，进入页面
    def get_page(self, response):
        page_list = response.xpath("//div[@id='wp_page_numbers']/ul/li/a/@href").extract()
        page_list.insert(0, response.url.split('/')[-1])
#        print(page_list)

        for j in page_list:
            page_url = 'http://www.meizitu.com/a/' + j
#            print(page_url)
            yield Request(url = page_url, callback = self.get_group)

#提取每页中的图组链接，进入图组页
    def get_group(self, response):
        group_list = response.xpath("//ul[@class='wp-list clearfix']/li/div/div/a/@href").extract()

        for group_url in group_list:
#            print(group_url)
            yield Request(url = group_url, callback = self.get_img)

#提取每张图片的链接
    def get_img(self, response):
        #print("Crawling page ----" + response.url + "----")
        item = MeizituItem()
        print(response)

#        item["category_name"] = category_name
#        print(item["category_name"])

        item["group_name"] = response.xpath("//div[@class='metaRight']/h2/a/text()").extract()
        print(item["group_name"])

        item["img_url_list"] = response.xpath("div[@id='picture']//p/img/@src").extract()
#        item["img_url_list"] = response.xpath("div[@id='postContent']//p/img/@src").extract()
        print(item["img_url_list"])

        item["img_name_list"] = response.xpath("div[@id='picture']//p/img/@alt").extract()
#        item["img_name_list"] = response.xpath("div[@id='postContent']//p/img/@alt").extract()
        print(item["img_name_list"])

#        yield item
