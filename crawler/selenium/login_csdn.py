#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'simulate login csdn'

import time
from selenium import webdriver
from selenium.common import exceptions


def work(driver):
    driver.maximize_window()
    driver.get("https://passport.csdn.net/account/login")
    driver.get_screenshot_as_file("login_before.jpg")

    try:
        elem_user = driver.find_element_by_name("username")
        elem_user.clear()
        elem_user.send_keys("kcoewoys@gmail.com")

        elem_pwd = driver.find_element_by_name("password")
        elem_pwd.clear()
        elem_pwd.send_keys("csdn**")
        elem_pwd.send_keys(webdriver.common.keys.Keys.ENTER)
    except exceptions.NoSuchElementException as e:
        print(e)
    except:
        print('failure')
    else:
        time.sleep(5)
        driver.get_screenshot_as_file("login_after.jpg")
        print(driver.title)


if __name__ == "__main__":
    #browser = webdriver.Firefox()
    browser = webdriver.PhantomJS()
    #browser = webdriver.Chrome()

    work(browser)

    browser.close()
    browser.quit()
