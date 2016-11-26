# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import urllib.request

class MeizituPipeline(object):
    def process_item(self, item, spider):
        path = 'output'
        category_name = item['category_name']
        group_name = item['group_name']

        if not os.path.exists(path):
            os.mkdir(path)

        if not os.path.exists(path + '/' + category_name):
            os.mkdir(path + '/' + category_name)

        if not os.path.exists(path + '/' + category_name + '/' + group_name):
            os.mkdir(path + '/' + category_name + '/' + group_name)

        f = open(path + "/url", "a")
        for i in range(0,len(item["img_urls"])):
            try:
                img_url = item["img_urls"][i]
                img_name = item['img_names'][i]

                file = path + '/' + category_name + '/' + group_name + '/' + img_name + '.jpg'
                f.write(img_url + '\t' + file + '\n')
                f.flush()
                print(img_url + '\t' + file)

#                urllib.request.urlretrieve(img_url, filename=file)

            except Exception as e:
                pass
        f.close()

        return item
