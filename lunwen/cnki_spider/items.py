# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CnkiSpiderItem(scrapy.Item):
    # all count is :17
    url = scrapy.Field()  #爬取的网页url
    MD5 = scrapy.Field()  #该论文网页唯一标识
    article_name = scrapy.Field()  #论文名字
    quote_num = scrapy.Field()  #引用数
    quoted_article_list_url = scrapy.Field() #引用该文章的其余文章列表
    publish_time = scrapy.Field()   #发表时间
    come_from_website_name = scrapy.Field() #来源网站
    come_from_website_url = scrapy.Field()  #来源网站的网址
    come_from_periodical = scrapy.Field()   #来源期刊等
    Include_author_name = scrapy.Field()    #查询的作者名字
    Include_author_name_En =scrapy.Field()  #查询的作者名字英文名正序
    Include_author_name_En2 = scrapy.Field()    #
    DepartmentName = scrapy.Field() #机构名字
    author_name_list = scrapy.Field()   #前几位作者列表
    IsFirstAuthor = scrapy.Field()  #查询的作者名字是否是第一作者
    abstract_Zh = scrapy.Field()    #中文摘要
    kw_main = scrapy.Field() #关键词
    doi = scrapy.Field() #DOI编号
    deep_search_word = scrapy.Field() #研究点分析

