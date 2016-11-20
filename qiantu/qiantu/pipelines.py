# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re
import os
import random
import urllib.request


class QiantuPipeline(object):
    def process_item(self, item, spider):
        if os.path.exists('./output') == False:
            os.mkdir('./output')

        for i in range(0, len(item["url"])):
            try:
                thisurl = item["url"][i]
                pat = "http://pic.qiantucdn.com/58pic/(.*?).jpg!qt"
                id = re.compile(pat).findall(thisurl)
                thistrueurl = "http://pic.qiantucdn.com/58pic/" + id[0] + "_1024.jpg"

                if os.path.exists('./output/' + item["folder_name"]) == False:
                    os.mkdir('./output/' + item["folder_name"])

#                避免名字重复，名字再加上个随机数
#                file="./output/"+id[-7:]+str(int(random.random()*10000))+".jpg"
                file = "./output/" + item['folder_name'] + "/" + thistrueurl.split('/')[-1]
                print(file)

                urllib.request.urlretrieve(thistrueurl, file)

            except Exception as e:
                pass

        return item
