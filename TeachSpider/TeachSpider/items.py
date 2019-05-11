# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TeachspiderItem(scrapy.Item):
    # define the fields for your item here like:
    TalentTitle = scrapy.Field()
    Tel = scrapy.Field()
    Email = scrapy.Field()
    MobilePhone = scrapy.Field()
    Education = scrapy.Field()
    Degree = scrapy.Field()
    ResearchField = scrapy.Field()

    Url = scrapy.Field()
    MD5= scrapy.Field()
    NameZh = scrapy.Field()
    NameEn1 = scrapy.Field()
    NameEn2 = scrapy.Field()
    SchoolName1 = scrapy.Field()
    DepartmentName = scrapy.Field()
    HtmlBody = scrapy.Field()

    SpiderTime = scrapy.Field()
