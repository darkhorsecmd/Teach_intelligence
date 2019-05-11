# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from tools.Get_all import Get_all
from tools.zhengze import zhengze as zz
from items import TeachspiderItem as items
from tools.format import format
import datetime


class TeachSpider(scrapy.Spider):
    name = 'Teach'
    start_urls = ['http://www.baidu.com/']

    def __init__(self):
        self.browser = webdriver.Chrome()
        super(TeachSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        # 爬虫退出的时候关闭浏览器
        self.browser.quit()

    def parse(self, response):
        datas = Get_all().get_all()  # '学校_学院1':[[name,url],[name2,url2]....], '学校_学院2':[[name,url],[name2,url2]....]
        for School_xueyuan_name, TeachList in datas.items():
            School_name = zz.get_Info(School_xueyuan_name, "xuexiao")
            xueyuan_name = zz.get_Info(School_xueyuan_name, "xueyuan")
            for Teach in TeachList:
                name = Teach[0]
                url = Teach[1]
                yield scrapy.Request(url=url, callback=self.parseDetail, dont_filter=True,
                                     meta={"xuexiao": School_name, "xueyuan": xueyuan_name, "name": name})

    def parseDetail(self, response):
        item = items()

        body = response.text
        item['HtmlBody'] = body

        item['Tel'] = zz.get_Info(body, "telnum")  # 电话号码
        item['TalentTitle'] = zz.get_Info(body, 'title')
        item['Email'] = zz.get_Info(zz.preclean(body), 'email')
        item['MobilePhone'] = zz.get_Info(body, 'phonenum')
        item['Education'] = zz.get_Info(body, 'education')
        item['Degree'] = zz.get_Info(body, 'degree')
        item['ResearchField'] = zz.get_Info(body, 'researchfield')

        item['SchoolName1'] = response.meta['xuexiao']
        item['DepartmentName'] = response.meta['xueyuan']
        item['NameZh'] = response.meta['name']
        item['NameEn1'] = format.tranPinyin(item['NameZh'])[0]  #正序
        item['NameEn2'] = format.tranPinyin(item['NameZh'])[1]  #逆序

        item['Url'] = response.url
        item['MD5'] =format.getMd5(item['NameZh']+item['SchoolName1']+item['DepartmentName']+item['Tel']+item['TalentTitle']+item['Email']+item['MobilePhone']+item['Education']+item['Degree']+item['ResearchField']+response.url)
        item['SpiderTime'] =datetime.datetime.now().strftime("%Y.%m.%d")

        yield item
