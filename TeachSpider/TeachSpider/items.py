# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TeachspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    telnum = scrapy.Field()
    email = scrapy.Field()
    phonenum = scrapy.Field()
    education = scrapy.Field()
    degree = scrapy.Field()
    researchfield = scrapy.Field()
