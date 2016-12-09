#!/usr/bin/env python3
#-*- coding:utf-8 -*-

'used to get port images'
__author__ = 'kcoewoys'

import re
import os
import queue
import threading
import urllib.request
from lxml import etree

class MyThread(threading.Thread):
    def __init__(self, img_id):
        super(MyThread, self).__init__()
        self.img_id = img_id
    def run(self):
        download(self.img_id)
        workqueue.task_done()
        print(self.name, 'finished!')

def download_thread():
    print('start main threading:')
    threads = [MyThread(workqueue.get()) for i in range(workqueue.qsize())]
    for t in threads:
        t.setDaemon(True)
        t.start()

    #wait the last thread
    for t in threads:
        t.join()
    print('end main threading.')

def download(img_id):
    lock.acquire()
    if not os.path.exists('output'):
        os.mkdir('output')
    lock.release()

    url = 'http://proxy.mimvp.com/common/ygrandimg.php?&port=' + img_id
    file_name = 'output/' + img_id + '.png'
    print(url + '\t' + file_name)
    try:
        urllib.request.urlretrieve(url, file_name)
    except urllib.error.URLError as e:
        print(e)
    except urllib.error.HTTPError as e:
        print(e)

def geturls(url, img_ids):
    header = ("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0")

    opener = urllib.request.build_opener()
    #use proxy ip
    #proxy = {'http':'122.96.59.105:843'}
    #proxy_handler = urllib.request.ProxyHandler(proxy);
    #opener = urllib.request.build_opener(proxy_handler)

    opener.addheaders = [header]
    urllib.request.install_opener(opener)
    try:
        data = urllib.request.urlopen(url).read()
    except urllib.error.HTTPError as e:
        print(e)
    else:
        et = etree.HTML(data.decode('utf-8'))
        port_img_urls = et.xpath('//td/img[not(@alt)]/@src')

        for url in port_img_urls:
            img_id = url.split('=')[-1]
            if img_id not in img_ids:
                img_ids.add(img_id)
                workqueue.put(img_id)
        download_thread()

    return img_ids

if __name__ == '__main__':
    img_ids = set()
    lock = threading.Lock()
    workqueue = queue.Queue()
    for i in range(1, 222):
        url = "http://proxy.mimvp.com/free.php?proxy=in_hp&page=" + str(i)
        print('\033[1;31;40m', url, '\033[0m')
        geturl = geturls(url, img_ids)
        if geturl:
            img_ids |= geturl
        else:
            break

    workqueue.join()
    print('\033[1;35;40m the number of images to be acquired is', len(img_ids), '\033[0m')

