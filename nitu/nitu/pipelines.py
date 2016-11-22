# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import urllib.request


class NituPipeline(object):
    def process_item(self, item, spider):
        path = 'output'
        if not os.path.exists(path):
            os.mkdir(path)

        t = open("output/url", "a")
        for i in range(len(item["pic_urls"])):
            try:
                pic_url = item["pic_urls"][i]

                if not os.path.exists(path + '/' +item["group_name"]):
                    os.mkdir(path + '/' + item["group_name"])

                file = path + '/' + item["group_name"] + '/' + item["pic_name"] + '.' + pic_url.split('.')[-1]
                t.write(file + '\n')
                t.flush()
                print(file)
#                urllib.request.urlretrieve(pic_url, filename=file)


            except Exception as e:
                pass
        t.close()

        return item
