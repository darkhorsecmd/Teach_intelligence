# -*- coding: utf-8 -*-
# @Time    : 2019/4/6 15:08
# @Author  : 郭增祥

import scrapy
from keji_post.items import ResearchInstitutionInfoItem
import requests
from scrapy.http import Request
from retrying import retry
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from lxml import etree
from keji_post.tools.format import format as f
import time
import csv
import os
from urllib.request import quote, unquote

class OutputNsfcSpider(scrapy.Spider):
    name = 'baike.baidu'
    allowed_domains = ['baike.baidu.com']
    start_urls = ['https://baike.baidu.com/item/%E9%A6%96%E9%83%BD%E5%8C%BB%E7%A7%91%E5%A4%A7%E5%AD%A6']

    count = 0

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # 'Cookie': 'BAIDUID=03386F21DD83E7D3EC1EF63CC923FA21:FG=1; BIDUPSID=03386F21DD83E7D3EC1EF63CC923FA21; PSTM=1551158999; delPer=0; PSINO=7; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; pgv_pvi=1474936832; pgv_si=s827367424; BDRCVFR[w2jhEs_Zudc]=mbxnW11j9Dfmh7GuZR8mvqV; BK_SEARCHLOG=%7B%22key%22%3A%5B%22%E6%B7%AE%E9%98%B4%E5%B7%A5%E5%AD%A6%E9%99%A2%E8%AE%A1%E7%AE%97%E6%9C%BA%E4%B8%8E%E8%BD%AF%E4%BB%B6%E5%B7%A5%E7%A8%8B%E5%AD%A6%E9%99%A2%22%2C%22%E6%B7%AE%E9%98%B4%E5%B7%A5%E5%AD%A6%E9%99%A2%22%2C%22%E6%B2%B3%E6%B5%B7%E5%A4%A7%E5%AD%A6%E8%AE%A1%E7%AE%97%E6%9C%BA%E4%B8%8E%E4%BF%A1%E6%81%AF%E5%AD%A6%E9%99%A2%22%2C%22http%3A%2F%2Fwww.jsfsc.edu.cn%22%2C%22%E6%B1%9F%E8%8B%8F%E9%A3%9F%E5%93%81%E5%AD%A6%E9%99%A2%22%2C%22%E6%B1%9F%E8%8B%8F%E4%BF%A1%E6%81%AF%E8%81%8C%E4%B8%9A%E5%AD%A6%E9%99%A2%22%5D%7D; Hm_lvt_55b574651fcae74b0a9f1cf9c8d7c93a=1552878333,1554518723,1554522400; H_PS_PSSID=1464_28802_21084_28769_28724_28557_28584_28518_28703; Hm_lpvt_55b574651fcae74b0a9f1cf9c8d7c93a=1554534606',
        'Host': 'baike.baidu.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
    }

    baseUrl = 'https://baike.baidu.com/item/'
    test_url = 'https://baike.baidu.com/item/%E9%A6%96%E9%83%BD%E5%8C%BB%E7%A7%91%E5%A4%A7%E5%AD%A6'
    def __init__(self):
        self.browser = webdriver.Chrome()
        super(OutputNsfcSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        # 爬虫退出的时候关闭浏览器
        self.browser.quit()

    @retry(stop_max_attempt_number=5)
    def parse(self, response):
        csv_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"\\data\\全国高校名单.csv"
        with open(csv_path, mode='r')as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            for row in csv_reader:
                if(line_count==0):
                    # print(f'Column names are {", ".join(row)}')
                    line_count += 1
                    continue
                # print(f'{row["学校名称"]}-{row["所在省"]}-{row["机构/学校编号"]}-{row["所在省"]}-{row["所在地市"]}-{row["主管部门"]}-{row["办学层次"]}-{row["办学性质"]}-{row["机构/学校标签"]}-{row["备注2"]}')
                line_count+=1
                url = OutputNsfcSpider.baseUrl+quote(row["学校名称"], encoding="utf-8")
                yield Request(url=url,callback=self.parseInfo,method="GET",headers=OutputNsfcSpider.headers,dont_filter=True,meta={"SchoolNum":row["机构/学校编号"],"SchoolNameZh":row["学校名称"],"Schoolgrade":row["机构/学校标签"],"Province":row["所在省"],"City":row["所在地市"],"Administration":row["主管部门"],"SchoolLevel":row["办学层次"],"private":row["办学性质"],"Note2":row["备注2"]})

    def parseInfo(self, response):
        item = ResearchInstitutionInfoItem()
        # 获取page数据
        try:
            if response.status != 200:
                try:
                    # 尝试使用chrome浏览器获得数据
                    print(response.status)
                    self.browser.get(str(response.url))
                    print()
                    self.page = etree.HTML(self.browser.page_source)
                    print(self.page)
                    print("page 获得完毕")
                except Exception as s:
                    print("chrom 浏览器异常")
                    print(s)
                    return
            else:
                # response.status ==200
                self.page = response
        except Exception as s1:
            print("数据获取异常:")
            print(s1)
            return


        # 防止值为空，预先赋一个空
        item['SchoolNum'] = ' '
        item['SchoolNameZh'] = ' '
        item['SchoolNameEn'] = ' '
        item['SchoolIntroduction'] = ' '
        item['Schoolgrade'] = ' '
        item['Province'] = ' '
        item['City'] = ' '
        item['Administration'] = ' '
        item['SchoolLevel'] = ' '
        item['private'] = ' '
        item['IntroductionUrl'] = ' '
        item['IntroductionContent'] = ' '
        item['SpiderTime'] = ' '
        item['Note2'] = ' '
        print("================================")
        try:
            f.getInfo(response=self.page,xpath_info='')
            item['SchoolNum'] = self.page.meta['SchoolNum']
            item['SchoolNameZh'] = self.page.meta['SchoolNameZh']
            item['SchoolNameEn'] = f.getInfo(response=self.page,xpath_info='//*[@class="basicInfo-block basicInfo-left"]//*[contains(text(),"英文名")]/following-sibling::dd[1]//text() |//*[@class="basicInfo-block basicInfo-left"]//*[contains(text(),"外文名")]/following-sibling::dd[1]//text()')
            item['SchoolIntroduction'] =' '
            item['Schoolgrade'] = self.page.meta['Schoolgrade']
            item['Province'] = self.page.meta['Province']
            item['City'] = self.page.meta['City']
            item['Administration'] = self.page.meta['Administration']
            item['SchoolLevel'] = self.page.meta['SchoolLevel']
            item['private'] = self.page.meta['private']
            item['IntroductionUrl'] = str(self.page.url)
            item['IntroductionContent'] = f.getInfo(response=self.page,xpath_info='//*[@class="lemma-summary"]//text()')
            item['SpiderTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            item['Note2'] = self.page.meta['Note2']
            print("当前爬取数量:" + str(OutputNsfcSpider.count))
            OutputNsfcSpider.count += 1
            yield item
        except Exception as e1:
            print("bbbbb")
            print(e1)
            print(str(OutputNsfcSpider.count))
            OutputNsfcSpider.count += 1
            yield item
