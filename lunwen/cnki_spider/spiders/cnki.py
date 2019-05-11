# -*- coding: utf-8 -*-
import time
import scrapy
from lxml import etree
from scrapy import signals
from selenium import webdriver
from scrapy.http import Request
from cnki_spider.tools.MD5 import selfMd5 as selfmd5
from scrapy.xlib.pydispatch import dispatcher
from selenium.webdriver.chrome.options import Options
from cnki_spider.tools.RandomUserAgent import RandomUserAgent as userAgent
from cnki_spider.items import CnkiSpiderItem as cnkiItem
from cnki_spider.tools.transerPinyin import transferPinyin
from cnki_spider.tools.constTool import MysqlPool as s_mysql
import configparser
import os
from cnki_spider.tools.chromes import NoProxy_Chrome as chromes
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class CnkiSpider(scrapy.Spider):
    name = 'cnki'
    allowed_domains = ['http://xueshu.baidu.com/']
    start_urls = ['http://xueshu.baidu.com/']
    count = 1

    def __init__(self):
        # 显示的调用父构造方法
        super(CnkiSpider, self).__init__()


        # self.cnki_browser = webdriver.Chrome()
        chromeTemp = chromes()
        self.cnki_browser = chromeTemp.get_chrome()
        self.first_browser = self.cnki_browser
        self.second_browser = self.cnki_browser

        #当爬虫关闭信号到来时候，调用关闭浏览器模块
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        #实例化一个userAgent更新
        self.RandomAgent = userAgent()


    def reset_chrome(self):
        self.cnki_browser.quit()
        time.sleep(1)
        self.cnki_browser = chromes().get_chrome()

    def spider_closed(self, spider):
        # 爬虫退出的时候关闭浏览器
        self.first_browser.quit()
        self.second_browser.quit()
        self.cnki_browser.quit()

    @classmethod
    def sendKey(cls,browser,NameZh,DepartmentName):
        #模拟在初始url中正常表单填写和点击
        base_url = 'http://xueshu.baidu.com/' #初始url
        try:
            browser.get(base_url)
        except Exception as e1:
            print(e1,"网页get失败")
        try:
            #元素查找
            Search_Input_button = browser.find_element_by_xpath('//input[@id="kw"]')
            Search_Click_button = browser.find_element_by_xpath('//input[@id="su"]')

            #模拟表单填写
            Search_Input_button.send_keys("author:("+NameZh+") "+DepartmentName)

            #模拟点击查询
            Search_Click_button.click()

        except Exception as e:
            print(e,"网页元素加载失败")

    @classmethod
    def find_info_num(cls,browser):
        #查找该教师的论文数量，百度学术多加了一个1，最后要减一
        num = browser.find_element_by_xpath('//*[@class="nums"]')
        return int(str(num.text).strip().replace("找到","").replace("条相关结果","").replace(",",""))-1

    @classmethod
    def find_each_info_element(cls,browser,response):
        #公共方法，返回一个查询页面一页的所有 article
        #返回类型为字典

        #页面数据结构
        try:
            info_dict = {}  #返回的页面字典
            article = {} #论文名字+论文超链接
            href_list = [] #超链接
            num_dict={}  #引用数 {[0,http:ss....],[0,https://www.ass],[1,https://www.asd]}
            year_list=[]  #发表年份
            len = 0  #info_dict里面元素公共长度
            info_dict['article'] = article
            info_dict['num_dict'] = num_dict
            info_dict['year_list']= year_list
            info_dict['len'] = 0
            info_dict['isLast'] = False

            bdxs_tree = etree.HTML(str(browser.page_source))
            element_list = bdxs_tree.xpath('//*[@class="result sc_default_result xpath-log"]')
            for element in element_list:
                #论文名字+论文超链接
                temp_article = []
                temp_article.append("".join(element.xpath('.//h3//text()')).replace("\n",""))
                # temp_article.append("".join("".join(element.xpath('.//h3//text()')).strip().split()))
                temp_article.append(response.urljoin("".join("".join(element.xpath('.//h3/a/@href')).strip().split())))
                article[len]=temp_article

                #发表年份
                year_list.append("".join(element.xpath('.//div[@class="sc_info"]//*[@class="sc_time"]//text()')).strip().replace("年",""))

                #引用次数
                num_inline = []
                if "".join("".join(element.xpath('.//*[@class="sc_info"]//span[contains(text(),"被引")]/a/text()')).strip().split()) is not None:
                    #引用数
                    num_inline.append("".join("".join(element.xpath('.//*[@class="sc_info"]//span[contains(text(),"被引")]/a/text()')).strip().split()))
                    #引用数指向的url
                    if "".join(element.xpath('.//a[contains(@href,"wd=refpaperuri")]/@href')) is not "":
                        num_inline.append(response.urljoin("".join(element.xpath('.//a[contains(@href,"wd=refpaperuri")]/@href'))))
                    else:
                        num_inline.append("")
                else:
                    num_inline.append('0')
                    num_inline.append('NULL')
                num_dict[len]=num_inline

                #正文超链接
                href_list.append(response.urljoin("".join(bdxs_tree.xpath('.//*[@class="sc_content"]/h3//a/@href'))))
                len+=1
            info_dict['len'] = len
            try:
                if browser.find_element_by_xpath('//*[@class="c-icon-pager-next"]') is None:  #探测是否下一页控件还有
                    info_dict['isLast'] = True
            except Exception:
                info_dict['isLast']= True  #如果捕获到了这个控件的异常，说明没有下一页了
            print("ok")
            return info_dict
        except Exception as e:
            print("find_each_info_element",e)
            return {}

    @classmethod
    def parse_numList(cls,browser,url,response):
        #开发者：每一次在使用该方法时候，一定要记得先browser.get(url)，不然这个browser的页面没有更新，获取的数据不对
        try:
            try:
                if url is not '':
                    browser.get(url=url)  #更改这个browser 重新申请一个browser
                    num_listAll = CnkiSpider.parse_articleList(browser=browser, response=response)
                    print("ok")
                    returns_list = []
                    for info_dict in num_listAll:
                        for i in range(info_dict['len']):
                            name_md5 = []
                            name_md5.append(info_dict['article'][i][0])
                            name_md5.append(selfmd5.getMd5(info_dict['article'][i][1]))
                            returns_list.append(name_md5)
                            print(info_dict)
                            print(name_md5)
                    print(returns_list)
                    return returns_list
            except Exception as parse1:
                print("url 为空，被正常捕获,尝试休眠3秒,再去访问该页面")
                return []
        except Exception as e:
            print("parse_numList",e)
        # browser = browser
        # #解析引用业的一些信息
        # browser.get(url=url)
        # num_listAll = self.parse_articleList(browser=browser,response=response)

    @classmethod
    def parse_articleList(cls,browser,response):
        #解析所有页的article，这里仅仅做逻辑，真正获取每页的数据依赖 find_each_info_element
        info_all = []
        Flag = True
        while Flag:
            info_dict = CnkiSpider.find_each_info_element(browser= browser,response=response)
            info_all.append(info_dict)
            if info_dict['isLast'] is False:
                url=response.urljoin(browser.find_element_by_xpath('//*[@class="c-icon-pager-next"]/ancestor::a[1]').get_attribute("href"))
                try:
                    browser.get(url=str(url).strip())
                except Exception as geturlE:
                    print("parse_articleList",geturlE)
                    print("ok parse_articleList")
            else:
                Flag = False
        return info_all

    def parse(self, response):
        #配置数据库连接
        cf = configparser.ConfigParser()
        config_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + "\\config\\Mysql_config.ini"
        cf.read(config_path)

        self.record = configparser.ConfigParser()
        self.record.read(os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + "\\config\\record.ini")

        school_mysql = s_mysql("Deparment_config")
        teache_mysql = s_mysql("Teach_config")

        school_TBName = cf.get("Deparment_config", "MYSQL_TBNAME")
        teache_TBName = cf.get("Teach_config","MYSQL_TBNAME")

        school_sql = "select * from "+school_TBName
        teache_sql = "select * from "+teache_TBName

        flag = True
        school_num  = int(school_mysql.getOne(sql="select count(*) from "+school_TBName)[0])
        school_datas = school_mysql.getAll(school_sql)
        if school_datas:
            for s_data in school_datas:
                school_name ={}
                #单个学校的中文名和英文名
                sc_zh = str(s_data[2])
                sc_en = str(s_data[3])
                teach_num =int(teache_mysql.getOne(sql="select count(*) from "+teache_TBName+" where SchoolName1=\'"+sc_zh+"\'")[0])
                if teach_num>0:
                    #查询到的该学校教师个数大于0
                    teach_datas  =teache_mysql.getAll(sql=teache_sql+" where SchoolName1=\'"+sc_zh+"\'")
                    all_name_list = []  #该学校所有教师存储list
                    id_num = 0
                    for teach_data in teach_datas:
                        teach_per = []  #单个教师所有属性
                        teach_per.append(str(teach_data[4]))  #中文名
                        teach_per.append(str(teach_data[5]))  #英文名
                        teach_per.append(str(teach_data[6]))  #英文名倒写
                        #初次运行一定要记得设置record.ini id字段为0
                        if teach_data[0]<=int(self.record.get("start_rbi_id","id")):
                            continue
                        all_name_list.append(teach_per)       #加入所有教师列表
                        id_num =teach_data[0]

                    #保存当前已经读取完毕的教师 ID，下一次运行将从record.ini 文件里面的id开始读
                    self.record.set("start_rbi_id","id",value=str(id_num))
                    record_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + "\\config\\record.ini"
                    self.record.write(open(record_path,"w"))

                    ###########sc_zh 存储学校中文名 sc_en存储英文名   all_name_list [0]:中文名  [1]:英文名正序 [2]:英文名倒叙
                    for per_datas in all_name_list:
                        for per_index in range(len(per_datas)):
                            NameZh =''
                            DepartmentName=''
                            if per_index ==0:
                                #中文名
                                NameZh = str(per_datas[per_index])
                                DepartmentName = sc_zh
                            if per_index == 1:
                                #英文名正序
                                NameZh = str(per_datas[per_index])
                                DepartmentName = sc_en
                            if per_index == 2:
                                #英文名倒序
                                NameZh = str(per_datas[per_index])
                                DepartmentName = sc_en

                            # NameZh = "张永军"
                            # DepartmentName = "淮阴工学院"
                            CnkiSpider.sendKey(browser=self.first_browser, NameZh=NameZh, DepartmentName=DepartmentName)
                            # 论文列表页信息
                            info_all = CnkiSpider.parse_articleList(browser=self.first_browser, response=response)

                            for info_dict in info_all:
                                for i in range(0, info_dict['len']):
                                    # CnkiSpider.count +=1
                                    # if(CnkiSpider.count %200 == 0):
                                    #     self.reset_chrome()
                                    # self.cnki_browser.delete_all_cookies()
                                    yield scrapy.Request(url=info_dict['article'][i][1], callback=self.parseDetail,
                                                         dont_filter=True,
                                                         meta={"article_name": info_dict['article'][i][0],
                                                                "num": info_dict['num_dict'][i][0],
                                                               "num_nameList_url": info_dict['num_dict'][i][1],
                                                               "year": info_dict['year_list'][i], "Name": NameZh,
                                                               "DepartmentName": DepartmentName})
                                    # 首先获得引用了这片文章的论文名字
                                    # yield scrapy.Request(url=info_dict['article'][i][1], callback=self.parseDetail,
                                    #                      dont_filter=True,
                                    #                      meta={"article_name": info_dict['article'][i][0],
                                    #                            "num": info_dict['num_dict'][i][0],
                                    #                            "num_nameList": CnkiSpider.parse_numList(
                                    #                                browser=self.second_browser,
                                    #                                url=info_dict['num_dict'][i][1], response=response),
                                    #                            "year": info_dict['year_list'][i], "Name": NameZh,
                                    #                            "DepartmentName": DepartmentName})

                    print("ok")
                else:
                    # 没有查询到该学校教师数据，直接跳过这个学校
                    # 后面考虑加上一个日志
                    print("该学校数据库教师信息为空", sc_zh)
                    continue
        #     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36'}
        #     headers['User-Agent']=self.RandomAgent.get_RanDomAgent()

    def parseDetail(self,response):
        item = cnkiItem()

        url = response.url
        MD5= selfmd5.getMd5(url)
        article_name = response.meta['article_name'] #论文名字
        if response.meta['num']=='':
            quote_num = '0'
        else:
            quote_num = response.meta['num']  #引用数
        quoted_article_list_url = response.urljoin(str(response.meta['num_nameList_url'])) #引用这篇论文的论文list_url
        publish_time = response.meta['year']  #该论文的发表年月
        come_from_website_name=''
        come_from_website_url=''
        come_from_periodical=''
        Include_author_name=''
        DepartmentName=''
        author_name_list=''
        abstract_Zh=''
        kw_main=''
        doi=''
        deep_search_word=''

        if response.xpath('//*[@class="label-ll"]/a/text()').extract_first() is not None:
            come_from_website_name =response.xpath('//*[@class="label-ll"]/a/text()').extract_first()

        if response.xpath('//*[@class="label-ll"]/a/@href').extract_first() is not None:
            come_from_website_url = response.xpath('//*[@class="label-ll"]/a/@href').extract_first()

        if response.xpath('//*[@class="journal_title"]/@title').extract_first() is not None:
            come_from_periodical = response.xpath('//*[@class="journal_title"]/@title').extract_first().replace('《','').replace('》','')

        Include_author_name = response.meta['Name']
        DepartmentName = response.meta['DepartmentName']

        IsFirstAuthor = True

        if "".join("".join(response.xpath('//*[@class="author_text"]//text()').extract()).strip().split()) is not None:
            author_name_list ="".join("".join(response.xpath('//*[@class="author_text"]//text()').extract()).strip().split())
            if author_name_list.split("，")[0] != response.meta['Name']:
                IsFirstAuthor = False

        if "".join(response.xpath('//*[@class="abstract"]//text()').extract()) is not None:
            abstract_Zh = "".join(response.xpath('//*[@class="abstract"]//text()').extract())

        if ",".join(response.xpath('//div[@class="kw_wr"]/p[@class="kw_main"]//text()').extract()) is not None:
            kw_main = ",".join(response.xpath('//div[@class="kw_wr"]/p[@class="kw_main"]//text()').extract())

        if response.xpath('//*[contains(text(),"DOI")]/following::p[1]/text()').extract_first() is not None:
            doi = response.xpath('//*[contains(text(),"DOI")]/following::p[1]/text()').extract_first()

        if ",".join(response.xpath('//div[@class="dtl_search_word"]//h3/following::div[1]//a/@title').extract()) is not None:
            deep_search_word = ",".join(response.xpath('//div[@class="dtl_search_word"]//h3/following::div[1]//a/@title').extract())

        item['url'] =url
        item['MD5'] =MD5
        item['article_name'] =article_name
        item['quote_num'] =quote_num
        item['quoted_article_list_url'] =str(quoted_article_list_url)
        item['publish_time'] =publish_time
        item['come_from_website_name'] =come_from_website_name
        item['come_from_website_url'] =come_from_website_url
        item['come_from_periodical'] =come_from_periodical
        item['Include_author_name'] =Include_author_name
        item['DepartmentName'] =DepartmentName
        item['author_name_list'] =author_name_list
        item['IsFirstAuthor'] =IsFirstAuthor
        item['abstract_Zh'] =abstract_Zh.replace("[","").replace("]","")
        item['kw_main'] =",".join("".join(kw_main.strip().replace(" ","").split(",")).split("\n"))
        item['doi'] =doi.strip()
        item['deep_search_word'] =deep_search_word
        yield item



