# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class KejiPostItem(scrapy.Item):
    # all_count  =14
    projectAdmin = scrapy.Field()  # 项目负责人姓名
    adminPosition = scrapy.Field()  # 负责人职称
    code = scrapy.Field()  # 申请代码
    conclusionAbstract = scrapy.Field()  # 结题摘要
    dependUnit = scrapy.Field()  # 依托单位
    projectAbstractC = scrapy.Field()  # 中文摘要
    projectAbstractE = scrapy.Field()  # 英文摘要
    projectKeywordC = scrapy.Field()  # 项目关键字
    projectKeywordE = scrapy.Field()  # 项目关键字英文
    projectName = scrapy.Field()  # 项目名称
    ratifyNo = scrapy.Field()  # 批准号
    researchTimeScope = scrapy.Field()  # 研究期限
    supportNum = scrapy.Field()  # 支持经费
    resultsList = scrapy.Field()  # 成果列表  type=list，里面再嵌套字典
    url = scrapy.Field() #访问的url
    supportClass = scrapy.Field()  #资助类别
    conclusionYear  =scrapy.Field() #结题年份