# -*- coding: utf-8 -*-
import scrapy
import re
from bing.items import BingItem


class GetimgSpider(scrapy.Spider):
    name = "getimg"
    allowed_domains = ["bing.com"]
    start_urls = ['https://cn.bing.com/']

    def parse(self, response):
        item = BingItem()
        item["background"] = re.findall(r'g_img={url: "(.*?)"',response.body.decode("utf-8"))
        yield item
