#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import time
import datetime
import socket
import sqlite3
import urllib.request
from lxml import etree

class getProxy():

    def __init__(self):
        self.user_agent = "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"
        self.header = {"User-Agent": self.user_agent}
        self.dbname="proxy.db"
        self.now = time.strftime("%Y-%m-%d")
        self.url = 'http://www.58pic.com/'

    def loop(self,page=5):
        for i in range(1,page):
            self.getContent(i)

    def getContent(self, num):

        #国内高匿
        url = "http://www.xicidaili.com/nn/" + str(num)
        try:
            req = urllib.request.Request(url, headers=self.header)
            html=urllib.request.urlopen(req).read()
        except urllib.error.HTTPError as e:
            print(e.code)
            print(e.read().decode("utf8"))

        et = etree.HTML(html.decode('utf-8'))
        ips = et.xpath('//tr/td[2]/text()')
        ports = et.xpath('//tr/td[3]/text()')

        for i in range(0, len(ips)):
#            print("IP:%s\tPort:%s" %(ips[i], ports[i]))
            if self.isAlive(ips[i], ports[i]):
                self.write_file(ips[i], ports[i])
                pass
#                self.insert_db(self.now, ips[i], ports[i])

    #查看爬到的代理IP是否还能用
    def isAlive(self,ip,port):
        proxy={'http':ip+':'+port}

        # 添加代理
        proxy_handler = urllib.request.ProxyHandler(proxy);
        opener = urllib.request.build_opener(proxy_handler)
        #将opener安装为全局
        urllib.request.install_opener(opener)
        req = urllib.request.Request(self.url, headers=self.header)

        #使用代理访问验证代理是否有效
#        socket.setdefaulttimeout(1)
        try:
            response = urllib.request.urlopen(req, timeout=2)
            if response.code==200:
                print(ip + ':' + port + "\tcan work")
                return True
            else:
                print(ip + ':' + port + "\tnot work")
                return False
        except :
            print(ip + ':' + port + "\terror")
            return False

    def insert_db(self, date, ip, port):
        dbname=self.dbname
        try:
            conn = sqlite3.connect(dbname)
        except:
            print("Error to open database%" %self.dbname)

        create_tb='CREATE TABLE IF NOT EXISTS PROXY(DATE TEXT,IP TEXT,PORT TEXT);'
        conn.execute(create_tb)
        insert_db_cmd="INSERT INTO PROXY (DATE,IP,PORT) VALUES ('%s','%s','%s');" %(date,ip,port)

        conn.execute(insert_db_cmd)
        conn.commit()
        conn.close()

    def write_file(self, ip, port):
        file = open('proxyip', 'a')
        proxy = ("     {'ip_port': '%s:%s', 'user_pass': ''},"%(ip,port))
        file.write(proxy + '\n')
        file.flush()
        file.close()

    #查看数据库里面的数据时候还有效，没有的话将其纪录删除
    def check_db_pool(self):
        conn=sqlite3.connect(self.dbname)
        query_cmd='select IP,PORT from PROXY;'
        cursor=conn.execute(query_cmd)
        for row in cursor:
            if not self.isAlive(row[0],row[1]):
                #代理失效， 要从数据库从删除
                delete_cmd="delete from PROXY where IP='%s'" %row[0]
                print("delete IP %s in db" %row[0])
                conn.execute(delete_cmd)
                conn.commit()

        conn.close()


if __name__ == "__main__":
    now = datetime.datetime.now()
    print("Start at %s" % now)
    obj=getProxy()
    obj.loop(5)
#    obj.check_db_pool()
