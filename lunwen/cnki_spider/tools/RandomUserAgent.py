# -*- coding: utf-8 -*-
# @Time    : 2019/4/17 13:20
# @Author  : 郭增祥
# @File    : RandomUserAgent-百度学术信息挖掘
from fake_useragent import UserAgent
#随机更换userAgent

class RandomUserAgent():
    def __init__(self):
        self.ua = UserAgent(verify_ssl=False)

    def get_RanDomAgent(self):
       return self.ua.random



if __name__ == '__main__':
    userAgent = RandomUserAgent()
    print(type(userAgent.get_RanDomAgent()))
    print(userAgent.get_RanDomAgent())