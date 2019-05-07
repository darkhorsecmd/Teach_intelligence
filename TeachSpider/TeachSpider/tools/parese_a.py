# -*- coding: utf-8 -*-
# @Time    : 2019/4/28 21:04
# @Author  : 郭增祥
# @File    : get_all_a-百度学术信息挖掘
from lxml import etree
from urllib.parse import urljoin
from TeachSpider.TeachSpider.tools.hanlp import hanlp as han


class parese_a(object):
    def __init__(self,chrome):
        self.chrome = chrome
        self.han = han()

    def set_url(self,url):
        self.Set_list(url=url)
        return self.get_all_a()

    def get_all_a(self):
        return self.han.set_a_list(self.a)

    def Set_list(self,url):
        self.pagesource = self.chrome.get(url=url)
        self.btree = etree.HTML(str(self.chrome.page_source))
        self.a =[]
        element_a_list =self.btree.xpath("//a")
        for element in element_a_list:
            each = []
            name = self.get_info(element=element, xpaths=".//text()")
            href = self.get_info(element=element,xpaths="./@href")
            href = urljoin(self.chrome.current_url,href)
            each.append(name)
            each.append(href)
            self.a.append(each)

    def get_info(self,element,xpaths):
        # print(element.xpath(xpaths))
        return "".join("".join(element.xpath(xpaths)).strip().split())

    def dispose(self):
        self.chrome.quit()

if __name__ == '__main__':
    from TeachSpider.TeachSpider.tools.chromes import NoProxy_Chrome as chrome
    parese = parese_a(chrome=chrome().get_chrome())
    all_a=parese.set_url("http://mgx.imu.edu.cn/szdw/mgyywxx.htm")
    print(all_a)
    parese.dispose()  #记得用退出
