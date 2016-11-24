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

        f = open("output/url", "a")
        try:
            pic_url = item["pic_url"][0]
            if not os.path.exists(path + '/' +item["group_name"]):
                os.mkdir(path + '/' + item["group_name"])

            file_name = path + '/' + item["group_name"] + '/' + item["pic_name"] + '.' + pic_url.split('.')[-1]
            f.write(pic_url + '\t' + file_name + '\n')
            f.flush()
            print(pic_url + '\t' + file_name)
#            urllib.request.urlretrieve(pic_url, filename=file_name)
        except Exception as e:
            pass

        f.close()

        return item
