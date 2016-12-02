# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class WeixinPipeline(object):
    def process_item(self, item, spider):
        for i in range(0, len(item['links'])):
            print(item['titles'][i])
            print(item['links'][i])
            print(item['abstracts'][i])
            print(item['times'][i])
            print(item['authors'][i])
            print('================================')

        return item
