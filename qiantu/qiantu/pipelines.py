# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re
import os
import urllib.request


class QiantuPipeline(object):
    def process_item(self, item, spider):
        path = 'output'
        if not os.path.exists(path):
            os.mkdir(path)

        for i in range(0, len(item["url"])):
            try:
                thisurl = item["url"][i]
                pat = "http://pic.qiantucdn.com/58pic/(.*?).jpg!qt"
                id = re.compile(pat).findall(thisurl)
                thistrueurl = "http://pic.qiantucdn.com/58pic/" + id[0] + "_1024.jpg"

                if not os.path.exists(path + '/' +item["folder_name"]):
                    os.mkdir(path + '/' + item["folder_name"])

                file = path + '/' + item['folder_name'] + '/' + thistrueurl.split('/')[-1]
                print(file)

#                urllib.request.urlretrieve(thistrueurl, file)

            except Exception as e:
                pass

        return item
