# -*- coding: utf-8 -*-
import scrapy
import json
from keji_post.items import KejiPostItem
import requests
from scrapy.http import Request
from retrying import retry
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
import jmespath as j
import ast
from lxml import etree
from fake_useragent import UserAgent
from keji_post.tools.Mylog import Mylog


class OutputNsfcSpider(scrapy.Spider):
    name = 'output.nsfc'
    allowed_domains = ['output.nsfc.gov']
    start_urls = ['http://output.nsfc.gov.cn/projectQuery']

    # sq_code = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']  # 申请代码
    # sq_code=['A01','A02','A03','A04','A05','B01','B02','B03','B04','B05','B06','B07','B08','B08','C01','C02','C03','C04','C05','C06','C07','C08','C09','C10','C11','C12','C13','C14','C15','C16','C17','C18','C19','C20','C21','D01','D02','D03','D04','D05','D06','D07','E01','E02','E03','E04','E05','E06','E07','E08','E09','F01','F02','F03','F04','F05','F06','F07','G01','G02','G03','G04','H01','H02','H03','H04','H05','H06','H07','H08','H09','H10','H11','H12','H13','H14','H15','H16','H17','H18','H19','H20','H21','H22','H23','H24','H25','H26','H27','H28','H29','H30','H31']
    # sq_code = ['A01','A02','A03','A04','A05','B01','B02','B03','B04','B05','B06','B07','B08','B08']  # 申请代码
    # sq_code = ['C01','C02','C03','C04','C05','C06','C07','C08','C09','C10','C11','C12','C13','C14','C15','C16','C17','C18','C19','C20','C21','D01','D02','D03','D04','D05','D06','D07']
    # sq_code = ['F', 'G', 'H']
    # self.sq_code = ['C02', 'C03']
    # zz_lei = ['218', '220', '222', '339', '429', '432', '649', '579', '630', '631', '632', '2699']  # 资助类别
    # self.zz_lei = ['218', '220', '222']
    count = 0
    all_num = 0
    # 提交的查询数据
    # payload = {"ratifyNo": "", "projectName": "", "personInCharge": "", "dependUnit": "", "code": "A",
    #            "projectType": "218", "subPType": "", "psPType": "", "keywords": "", "ratifyYear": "",
    #            "conclusionYear": "2017", "beginYear": "", "endYear": "", "checkDep": "", "checkType": "",
    #            "quickQueryInput": "", "adminID": "", "pageNum": 0, "pageSize": 5, "queryType": "input",
    #            "complete": "true"}

    # 请求查询list的headers

    # 请求详细信息的headers

    baseUrl = 'http://output.nsfc.gov.cn/baseQuery/data/conclusionQueryResultsData'
    infoUrl = 'http://output.nsfc.gov.cn/baseQuery/data/conclusionProjectInfo/'
    ua = UserAgent(verify_ssl=False)  #设置user-agent

    def change_UserAgent(self):
        self.headers['User-Agent'] = OutputNsfcSpider.ua.random
        self.infoHeaders['User-Agent'] = OutputNsfcSpider.ua.random

    def __init__(self):
        self.browser = webdriver.Chrome()
        super(OutputNsfcSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)  #给chrome提供爬虫结束信号
        self.headers={
        'Host': 'output.nsfc.gov.cn',
        'Connection': 'keep-alive',
        'Content-Length': '334',
        'Accept': '*/*',
        'Origin': 'http://output.nsfc.gov.cn',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
        'Content-Type': 'application/json',
        'Referer': 'http://output.nsfc.gov.cn/projectQuery',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
        self.infoHeaders = {
        'Host': 'output.nsfc.gov.cn',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }

        # 记录一下状态码不是200的url
        self.logs = Mylog("not200")

    def spider_closed(self, spider):
        # 爬虫退出的时候关闭浏览器
        self.browser.quit()

    @retry(stop_max_attempt_number=5)
    def parse(self, response):
        # sq_code = ['B03','B04','B01','B02','A01','A02','A03','A04','A05']
        sq_code=['B05','B06','B07','B08','B08','C01','C02','C03','C04','C05','C06','C07','C08','C09','C10','C11','C12','C13','C14','C15','C16','C17','C18','C19','C20','C21','D01','D02','D03','D04','D05','D06','D07']
        zz_lei = ['218', '220', '222', '339', '429', '432', '649', '579', '630', '631', '632', '2699']  # 资助类别
        for sq in range(len(sq_code)):
            for zz in zz_lei:
                OutputNsfcSpider.all_num = 0
                for year in range(1970, 2019):
                    payload = {"ratifyNo": "", "projectName": "", "personInCharge": "", "dependUnit": "", "code": "",
                               "projectType": "", "subPType": "", "psPType": "", "keywords": "", "ratifyYear": "",
                               "conclusionYear": "", "beginYear": "", "endYear": "", "checkDep": "",
                               "checkType": "",
                               "quickQueryInput": "", "adminID": "", "pageNum": 0, "pageSize": 5, "queryType": "input",
                               "complete": "true"}
                    y = str(year)
                    self.change_UserAgent()  # 随机更换下User_Agent
                    payload['pageNum'] = 0  # 每一次迭代之前，页码肯定为0开始
                    payload['code'] = sq_code[sq]  # 申请代码
                    payload['projectType'] = zz  # 申请类别
                    payload['conclusionYear'] = y  # 申请年份

                    if(len(zz)==4):
                        self.headers['Content-Length'] = '337'
                    else:
                        self.headers['Content-Length']='336'
                    res = requests.post(url=self.baseUrl, data=json.dumps(payload), headers=self.headers,
                                        timeout=20)
                    js = json.loads(res.text)
                    flag = True
                    OutputNsfcSpider.all_num += int(js['data']['iTotalRecords'])
                    current = js['data']['iTotalRecords']
                    while (flag):
                        if "Error" in res.text:
                            print("Error in res text")
                            flag = False
                            continue
                        if len(js['data']['resultsData']) != 0:
                            for i in js['data']['resultsData']:
                                hz_num = i[2]  #获取后缀
                                # for i in range(len(js['data']['resultsData'])):
                                #     hz_num = js['data']['resultsData'][i][2]  # 获取每一个网页的后缀
                                url = self.infoUrl + hz_num
                                yield Request(url=url, encoding='utf-8', dont_filter='True',
                                              headers=self.infoHeaders, callback=self.parseInfo,
                                              meta={"url": url, "supportClass": zz, "conclusionYear": y})
                            payload['pageNum'] += 1  # 页码加一

                            #调试发现 Content-Length会随着payload的字符个数增加而增加
                            if (payload['pageNum'] >= 10000):
                                self.headers['Content-Length'] = '340'
                            if(payload['pageNum']>=1000):
                                self.headers['Content-Length'] = '339'
                            elif(payload['pageNum']>=100):
                                self.headers['Content-Length'] = '338'
                            elif(payload['pageNum']>=10):
                                self.headers['Content-Length'] = '337'
                            else:
                                self.headers['Content-Length'] = '336'
                            print(sq, zz, y, "数据总量",current,"pay load 当前页",payload['pageNum'],"pay load长度",self.headers['Content-Length'])
                            res = requests.post(url=self.baseUrl, data=json.dumps(payload), headers=self.headers,
                                                timeout=20)
                            js = json.loads(res.text)
                            print(js)
                        else:
                            flag = False
                            continue
                print("执行到了下一个类别")
                try:
                    self.logs.info("申请代码" + sq_code[sq] + "-类别" + zz + "查询到了" + str(OutputNsfcSpider.all_num) + "条数据")
                    print("log requests")
                except Exception as e1:
                    print(e1)

    def parseInfo(self, response):
        item = KejiPostItem()
        page = ''
        # 获取page数据
        try:
            if response.status != 200:
                print("record one not 200")
            else:
                # response.status ==200
                page = str(response.text)
                # 转换为字典
                try:
                    self.data = eval(page)  # 将str属性的page 转为dict属性
                    print(type(self.data))
                except Exception as e:
                    print(self.data)
                    print("数据异常2：")
                    print(e)
                    yield
                # 防止值为空，预先赋一个空
                item['projectAdmin'] = ' '
                item['adminPosition'] = ' '
                item['code'] = ' '
                item['conclusionAbstract'] = ' '
                item['dependUnit'] = ' '
                item['projectAbstractC'] = ' '
                item['projectAbstractE'] = ' '
                item['projectKeywordC'] = ' '
                item['projectKeywordE'] = ' '
                item['projectName'] = ' '
                item['ratifyNo'] = ' '
                item['researchTimeScope'] = ' '
                item['supportNum'] = '无'
                item['resultsList'] = ' '
                print("================================")
                try:
                    if (j.search("data.projectAdmin", self.data) != ''):
                        item['projectAdmin'] = j.search("data.projectAdmin", self.data)
                    if (j.search("data.adminPosition", self.data) != ''):
                        item['adminPosition'] = j.search("data.adminPosition", self.data)
                    if (j.search("data.code", self.data) != ''):
                        item['code'] = j.search("data.code", self.data)
                    if (j.search("data.conclusionAbstract", self.data) != ''):
                        item['conclusionAbstract'] = j.search("data.conclusionAbstract", self.data)
                    if (j.search("data.dependUnit", self.data) != ''):
                        item['dependUnit'] = j.search("data.dependUnit", self.data)
                    if (j.search("data.projectAbstractC", self.data) != ''):
                        item['projectAbstractC'] = j.search("data.projectAbstractC", self.data)
                    if (j.search("data.projectAbstractE", self.data) != ''):
                        item['projectAbstractE'] = j.search("data.projectAbstractE", self.data)
                    if (j.search("data.projectKeywordC", self.data) != ''):
                        item['projectKeywordC'] = j.search("data.projectKeywordC", self.data)
                    if (j.search("data.projectKeywordE", self.data) != ''):
                        item['projectKeywordE'] = j.search("data.projectKeywordE", self.data)
                    if (j.search("data.projectName", self.data) != ''):
                        item['projectName'] = j.search("data.projectName", self.data)
                    if (j.search("data.ratifyNo", self.data) != ''):
                        item['ratifyNo'] = j.search("data.ratifyNo", self.data)
                    if (j.search("data.researchTimeScope", self.data) != ''):
                        item['researchTimeScope'] = j.search("data.researchTimeScope", self.data)
                    if (j.search("data.supportNum", self.data) != ''):
                        item['supportNum'] = j.search("data.supportNum", self.data)
                    if (j.search("data.supportNum", self.data) != ''):
                        item['supportNum'] = j.search("data.supportNum", self.data) + "万元"
                    # resultlist 字段返回为[] 或者里面有数据
                    item['resultsList'] = str(j.search("data.resultsList", self.data))
                    item['url'] = response.meta["url"]
                    item['supportClass'] = response.meta["supportClass"]  # 资助类别
                    item['conclusionYear'] = response.meta["conclusionYear"]  # 结题年份

                    print("当前爬取数量:" + str(OutputNsfcSpider.count))
                    OutputNsfcSpider.count += 1
                    yield item
                except Exception as e1:
                    print("bbbbb")
                    print(e1)
                    print(str(OutputNsfcSpider.count))
                    OutputNsfcSpider.count += 1
                    yield

        except Exception as s1:
            print("数据获取异常:")
            print(s1)
            yield

