# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NituItem(scrapy.Item):
    # define the fields for your item here like:
    pic_urls = scrapy.Field()
    pic_name = scrapy.Field()
    group_name = scrapy.Field()
