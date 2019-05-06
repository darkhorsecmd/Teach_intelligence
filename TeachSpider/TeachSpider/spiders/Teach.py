# -*- coding: utf-8 -*-
import scrapy


class TeachSpider(scrapy.Spider):
    name = 'Teach'
    allowed_domains = ['Teach.com']
    start_urls = ['http://Teach.com/']

    def parse(self, response):
        pass
