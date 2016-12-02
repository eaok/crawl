# -*- coding: utf-8 -*-

import scrapy
from weixin.items import WeixinItem


class WechatSpider(scrapy.Spider):
    name = "wechat"
    allowed_domains = ["weixin.sogou.com"]
    start_urls = ['http://weixin.sogou.com/']

    def parse(self, response):
        key = 'machine learning'
        for i in range(0, 2):
            current_page = 'http://weixin.sogou.com/weixin?query=' + str(key) + '&type=2&page=' + str(i)
            yield scrapy.Request(current_page, callback=self.parse_page)

    def parse_page(self, response):
        item = WeixinItem()
        item_node = response.xpath("//div[@class='txt-box']/h3/a")
        item["titles"] = item_node.xpath('string(.)').extract()
        item["links"] = item_node.xpath("./@href").extract()

        item_node1 = response.xpath("//p[@class='txt-info']")
        item["abstracts"] = item_node1.xpath('string(.)').extract()

        item['times'] = response.xpath('//div[@class="s-p"]/a/text()').extract()
        item['authors'] = response.xpath('//span[@class="s2"]/text()').extract()

        yield item
