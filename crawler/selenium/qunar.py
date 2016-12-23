#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
#import win32api
#import win32con
from lxml import etree
from selenium import webdriver


def fill():
    browser.get("http://flight.qunar.com/")  # cookie保存在对象中，对需认证页面可直接访问
    browser.get_screenshot_as_file("./home.jpg")

    browser.find_element_by_id("searchTypeSng").click()  # 设置为单程
    fromcity = browser.find_element_by_xpath('//*[@id="dfsForm"]/div[2]/div[1]/div/input')
    fromcity.clear()
    fromcity.send_keys("北京")  # 置出发地点
    print('sleep 1')
    time.sleep(1)
    fromcity.send_keys(webdriver.common.keys.Keys.ENTER)
    # 按某个键 win32api.keybd_event(键位码, 0, 0, 0)
    # 释放按键 win32api.keybd_event(键位码, 0, win32con.KEYEVENTF_KEYUP, 0)
    # win32api.keybd_event(108, 0, 0, 0)  # enter键
    # win32api.keybd_event(108, 0, win32con.KEYEVENTF_KEYUP, 0)  # 放开按键

    tocity = browser.find_element_by_xpath('//*[@id="dfsForm"]/div[2]/div[2]/div/input')
    tocity.clear()
    tocity.send_keys("上海")  # 设置目的地
    print('sleep 2')
    time.sleep(1)
    tocity.send_keys(webdriver.common.keys.Keys.ENTER)
    # win32api.keybd_event(108, 0, 0, 0)
    # win32api.keybd_event(108, 0, win32con.KEYEVENTF_KEYUP, 0)

    browser.find_element_by_xpath('//*[@id="fromDate"]').clear()
    browser.find_element_by_xpath('//*[@id="fromDate"]').send_keys("2016-12-24")
    print('sleep 3')
    time.sleep(1)
    browser.find_element_by_xpath('//*[@id="fromDate"]').click()
    browser.find_element_by_xpath('//*[@id="dfsForm"]/div[4]/button').click()  # 点击按钮 提交表单
    print('sleep 4')
    time.sleep(5)


def filters(data):
    # flytitleall = [i.text for i in browser.find_elements_by_xpath('//div[@class="air"]/span')]
    et = etree.HTML(data)
    flytitleall = et.xpath('//div[@class="air"]/span/text()')

    return flytitleall


def echos(page, flytitleall):
    browser.get_screenshot_as_file("./page_" + str(page) + ".jpg")

    print("第"+str(page)+"页的数据是：")
    print(flytitleall)
    # for j in range(0,len(flytitleall)):
    #     print(flytitleall[j])
    #     print("-------")

if __name__ == '__main__':
    start = time.time()
    browser = webdriver.PhantomJS()
    browser.maximize_window()  # 浏览器窗口最大化
    fill()
    current = time.time()
    print("current cost time: %s" % (current-start))

    for k in range(0, 3):
        data = browser.page_source
        print(browser.current_url)

        flytitleall = filters(data)
        echos(k+1, flytitleall)
        browser.find_element_by_xpath('//*[@class="container"]/a[text()="下一页"]').click()

    browser.quit()
    end = time.time()
    print("cost all time: %s" % (end-start))

