# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import urllib.request

class WallpaperPipeline(object):
    def process_item(self, item, spider):
        if os.path.exists('./output') == False:
            os.mkdir('./output')

        if os.path.exists('./output/' + item['category_name']) == False:
            os.mkdir('./output/' + item['category_name'])

        if os.path.exists('./output/' + item['category_name'] + '/' + item['group_name']) == False:
            os.mkdir('./output/' + item['category_name'] + '/' + item['group_name'])

        for i in range(0,len(item["img_url_list"])):
            try:
                img_url = item["img_url_list"][i]
                true_img_url = img_url.replace('/t/', '/pic/')
                print(true_img_url)

#                file = "./output/" + item['category_name'] + "/" + item['group_name'] + "/"
                file = "./output/" + item['category_name'] + "/" + item['group_name'] + '/' + true_img_url.split('/')[-1]

                print(file)

                urllib.request.urlretrieve(true_img_url, file)

            except Exception as e:
                pass
        return item

