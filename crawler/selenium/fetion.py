#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from selenium import webdriver

'''
Login fetion and send message
'''


def work(driver):
    driver.maximize_window()
    driver.get("http://webim.feixin.10086.cn/")
    #browser.set_page_load_timeout(10)
    #time.sleep(5)
    #print('2')

    try:
        driver.get_screenshot_as_file("login_before.jpg")

        driver.switch_to_frame('loginform')  # 进入到iframe
        #driver.find_element_by_id("login_username").clear()
        driver.find_element_by_id("login_username").send_keys("18720984497")

        driver.find_element_by_id("getSmsPwd").click()
        print('please input the captcha')
        captcha = input()

        elem_pwd = driver.find_element_by_id("login_pass1")
        elem_pwd.send_keys(captcha)
        #elem_pwd.send_keys(webdriver.common.keys.Keys.ENTER)

        driver.find_element_by_id("btnlogin").click()
        time.sleep(5)
        driver.switch_to_default_content()  # 跳出iframe，回到主content

    except Exception as e:
        print(e)
    else:
        
        driver.get_screenshot_as_file("login_after.jpg")
        print(driver.title)


if __name__ == "__main__":
    # browser = webdriver.Firefox()
    # browser = webdriver.PhantomJS()
    browser = webdriver.Chrome()

    work(browser)

    #browser.close()
    #browser.quit()
