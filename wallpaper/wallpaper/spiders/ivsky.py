# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from wallpaper.items import WallpaperItem

global category_name
global group_name
category_name = ""
group_name = ""

class IvskySpider(scrapy.Spider):
    name = "ivsky"
    allowed_domains = ["ivsky.com/bizhi/1920x1080"]
    start_urls = ['http://ivsky.com/bizhi/1920x1080/']

#提取所有的分类链接，进入分类页
    def parse(self, response):
        global category_name
        category_url_list = response.xpath("//ul[@class='bzmenu']/li[position()>1]/a/@href").extract()
        category_name_list = response.xpath("//ul[@class='bzmenu']/li[position()>1]/a/text()").extract()
#        print(category_url_list)
#        print(category_name_list)

        for i in range(0, len(category_url_list)):
            category_url = "http://www.ivsky.com" + category_url_list[i]
            category_name = category_name_list[i]
#            category_name = category_url.split('/')[-2]
#            print(category_url)
#            print(category_name)
            yield Request(url = category_url, callback = self.get_page, dont_filter = True)

#提取页数链接，进入页面
    def get_page(self, response):
        print("\n\nCrawling page " + "@@@@@@@@@@@@@@@@@@@@  category  @@@@@@@@@@@@@@@@@@@@@@@@@ " + response.url)
        page_list = response.xpath("//div[@class='pagelist']/a/@href").extract()
        page_list.insert(0, response.url[20:])
#        page_list.insert(0, '/' + response.url.split('/')[-2] + response.url.split('/')[-1])
#        print(page_list)

        for j in range(0, len(page_list) - 1):
            page_url = 'http://www.ivsky.com' + page_list[j]
#            print(page_url)
            yield Request(url = page_url, callback = self.get_group, dont_filter = True)

#提取每页中的图组链接，进入图组页
    def get_group(self, response):
        global group_name
        print("\n\nCrawling page " + "||||||||||||||||||||    page    ||||||||||||||||||||||||| " + response.url)
        group_url_list = response.xpath("//ul[@class='ali']/li/div/a/@href").extract()
        group_name_list = response.xpath("//ul[@class='ali']/li/div/a/@title").extract()

        for k in range(0,len(group_url_list)):
            group_url = "http://www.ivsky.com" + group_url_list[k]
            group_name = group_name_list[k]
#            print(group_url)
#            print(group_name)
            yield Request(url = group_url, callback = self.get_img, dont_filter = True)

#提取每张图片的链接,返回给item
    def get_img(self, response):
        global category_name
        global group_name
        print("\n\nCrawling page " + "====================   group   ========================== " + response.url)
        item = WallpaperItem()

        item["img_url_list"] = response.xpath("//ul[@class='pli']/li/div/a/img/@src").extract()
        item["category_name"] = category_name
        item["group_name"] = group_name
#        print(item)
        yield item

        next_page = response.xpath("//div[@class='pagelist']/a[@class='page-next']/@href").extract_first()
        if next_page:
            next_page_url = "http://www.ivsky.com" + next_page
#            print(next_page_url + "==================================================")
#            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page_url, callback = self.get_img, dont_filter = True)

