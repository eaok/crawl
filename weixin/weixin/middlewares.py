# -*- coding: utf-8 -*-

import random
from weixin.settings import PROXIES
from weixin.settings import USER_AGENT
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware


class RandomUserAgent(object):
    """Randomly rotate user agents based on a list of predefined ones"""
    def __init__(self, user_agent=''):
        self.user_agent = user_agent

    def process_request(self, request, spider):
        self.user_agent = random.choice(USER_AGENT)
        if self.user_agent:
            try:
                request.headers.setdefault('User-Agent', self.user_agent)
                print("************************************************** use user_agent")
            except Exception as e:
                pass

class ProxyMiddleware(HttpProxyMiddleware):
    """Randomly rotate proxy based on a list of predefined ones"""
    def __init__(self, proxy=''):
        self.proxy = proxy

    def process_request(self, request, spider):
        self.proxy = random.choice(PROXIES)
        print("************************************************** use proxy\t" + self.proxy['ipaddr'])
        if self.proxy:
            try:
                request.meta["proxy"] = "http://" + self.proxy["ipaddr"]
            except Exception as e:
                pass
