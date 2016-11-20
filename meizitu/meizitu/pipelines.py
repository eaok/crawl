# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import urllib.request

class MeizituPipeline(object):
    def process_item(self, item, spider):
        if os.path.exists('./output') == False:
            os.mkdir('./output')
        if os.path.exists('./output/' + item["category_name"]) == False:
            os.mkdir('./output/' + item["category_name"])


        for i in range(0,len(item["img_url_list"])):
            try:
                img_url=item["img_url_list"][i]
                print(img_url)

                file = "./output/" + item["category_name"] + "/" + item["category_name"][i] + "." + item["img_url_list"][i].split('.')[-1]
                print(file)
                #urllib.request.urlretrieve(img_url,filename=file)

            except Exception as e:
                pass
        return item
