# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QiantuItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    folder_name = scrapy.Field()
