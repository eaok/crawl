#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from selenium import webdriver

'''
Login yeah email
'''


def work(driver):
    driver.maximize_window()
    browser.set_page_load_timeout(10)
    driver.get("http://yeah.net/")
    time.sleep(5)

    try:
        driver.get_screenshot_as_file("login_before.jpg")

        driver.switch_to_frame('x-URS-iframe')  # 进入到iframe
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
        time.sleep(5)
        driver.get_screenshot_as_file("login_after.jpg")
        print(driver.title)


if __name__ == "__main__":
    browser = webdriver.Firefox()
    # browser = webdriver.PhantomJS()
    # browser = webdriver.Chrome()

    work(browser)

    browser.close()
    browser.quit()
