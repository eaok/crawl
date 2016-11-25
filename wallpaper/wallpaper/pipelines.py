# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import urllib.request

class WallpaperPipeline(object):
    def process_item(self, item, spider):
        path = 'output'
        if not os.path.exists(path):
            os.mkdir(path)

        if not os.path.exists(path + '/' + item['category_name']):
            os.mkdir(path + '/' + item['category_name'])

        if not os.path.exists(path + '/' + item['category_name'] + '/' + item['group_name']):
            os.mkdir(path + '/' + item['category_name'] + '/' + item['group_name'])

        f = open("output/url", "a")
        for i in range(0,len(item["img_urls"])):
            try:
                img_url = item["img_urls"][i]
                true_img_url = img_url.replace('/t/', '/pic/')

                file_name = path + '/' + item['category_name'] + "/" + item['group_name'] + '/' + true_img_url.split('/')[-1]
                print(true_img_url + '\t' + file_name)
                f.write(true_img_url + '\t' + file_name + '\n')
                f.flush()

#                urllib.request.urlretrieve(true_img_url, file_name)

            except Exception as e:
                pass
        f.close()

        return item

