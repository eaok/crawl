#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Login yeah email
'''

import time
from selenium import webdriver


def work(driver):
    driver.maximize_window()
    browser.set_page_load_timeout(15)
    driver.get("http://yeah.net/")
    time.sleep(5)

    try:
        driver.get_screenshot_as_file("login_before.jpg")

        # driver.switch_to_frame('x-URS-iframe')  # 进入到iframe,这种PhantomJS用不了
        driver.switch_to_frame(1)  # chorme需要为0
        driver.find_element_by_name("email").clear()
        driver.find_element_by_name("email").send_keys("kcoewoys")

        elem_pwd = driver.find_element_by_name("password")
        elem_pwd.clear()
        elem_pwd.send_keys("**")

        # elem_pwd.send_keys(webdriver.common.keys.Keys.ENTER)
        driver.find_element_by_id("dologin").click()
        driver.switch_to_default_content()  # 跳出iframe，回到主content

    except Exception as e:
        print(e)
    else:
        time.sleep(9)
        driver.get_screenshot_as_file("login_after.jpg")
        print(driver.title)


if __name__ == "__main__":
    # browser = webdriver.Firefox()
    browser = webdriver.PhantomJS()
    # browser = webdriver.Chrome()

    work(browser)

    browser.quit()
