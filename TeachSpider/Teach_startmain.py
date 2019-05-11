# -*- coding: utf-8 -*-
# @Time    : 2019/3/28 16:31
# @Author  : 郭增祥
import sys
import os
from scrapy.cmdline import execute
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# execute(["scrapy","crawl","output.nsfc"])
execute(["scrapy","crawl","Teach","-s","LOG_FILE=Teach.log"])

# TO DO 执行完爬虫后，将SChool_list_data 目录下的所有文件移到 data_read_ok目录

