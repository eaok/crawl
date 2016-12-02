# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import random
import urllib.request
from meizitu.settings import USER_AGENT

class MeizituPipeline(object):
    def process_item(self, item, spider):
        path = 'output'
        category_name = item['category_name']
        group_name = item['group_name'].replace('，', '_').replace('！', '_').replace('、', '_')

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
                img_name = item['img_names'][i].replace(' ','').replace('，', '_').replace('！','_').replace('、', '_')

                file_name = path + '/' + category_name + '/' + group_name + '/' + img_name + '.jpg'
                f.write(img_url + '\t' + file_name + '\n')
                f.flush()
                print(img_url + '\t' + file_name)

                user_agent = random.choice(USER_AGENT)
                opener=urllib.request.build_opener()
                opener.addheaders=['User-Agent',user_agent]
                urllib.request.install_opener(opener)
                urllib.request.urlretrieve(img_url, filename=file_name)
                print(img_url +'\t==================================================================' )

            except Exception as e:
                pass
        f.close()

        return item
