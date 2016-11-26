# -*- coding: utf-8 -*-
import random
import base64
from meizitu.settings import PROXIES
from meizitu.settings import USER_AGENT

class RandomUserAgent(object):
    """Randomly rotate user agents based on a list of predefined ones"""
    def __init__(self, user_agents=''):
        self.user_agents = user_agents

    def process_request(self, request, spider):
        user_agent = random.choice(USER_AGENT)
        if user_agent:
            request.headers.setdefault('User-Agent', user_agent)
            print("************************************************** use user_agent")

# Start your middleware class
class ProxyMiddleware(object):
    # overwrite process request
    def process_request(self, request, spider):
        proxy = random.choice(PROXIES)

        if proxy['user_pass'] == '':
            pass
            print("************************************************** Proxy no pass\t" + proxy['ip_port'])
            request.meta['proxy'] = "http://" + proxy['ip_port']
        else:
            print("************************************************** Proxy have pass\t" + proxy['ip_port'])
            request.meta['proxy'] = "http://" + proxy['ip_port']
            encoded_user_pass = base64.b64encode(proxy['user_pass'].encode(encoding="utf-8"))
            request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass.decode()

