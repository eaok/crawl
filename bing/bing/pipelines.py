# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import urllib
import os

def get_file(url):
    try:
        data = urllib.request.urlopen(url).read()
        #data = str(data)
        return data
    except BaseException as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
        return None


class BingPipeline(object):
    def process_item(self, item, spider):
        if os.path.exists('./output') == False:
            os.mkdir('./output')

        url = 'https://cn.bing.com' + item["background"][0]
#        print(url)

        f = open('./output/' + url.split('/')[-1], "wb")
        f.write(get_file(url))
        f.flush()
        f.close()
        print("Successfully generated " + "./output/" + url.split('/')[-1] + "!")

        return item
