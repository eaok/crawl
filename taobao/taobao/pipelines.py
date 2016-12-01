# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql

class TaobaoPipeline(object):
    def __init__(self):
        # 连接mysql
        #self.conn = pymysql.connect(host="127.0.0.1",port=3306,user="root",passwd="123456",db="mydb",charset='UTF8')
        config = {
            'host':'127.0.0.1',
            'port':3306,
            'user':'root',
            'password':'123456',
            'db':'mydb',
            'charset':'utf8'
        }
        self.conn = pymysql.connect(**config)

        # 创建游标
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        try:
            title=item["title"][0]
            link=item["link"]
            price=item["price"][0]
            comment=item["comment"][0]

            sql="insert into goods(title,link,price,comment) values('"+title+"','"+link+"','"+price+"','"+comment+"')"
            print(sql)
            self.cursor.execute(sql)

            # 提交，不然无法保存新建或者修改的数据
            self.conn.commit()
            return item

        except Exception as err:
            pass

    def close_spider(self):
        self.cursor.close()
        self.conn.close()
