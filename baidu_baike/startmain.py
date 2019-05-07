# -*- coding: utf-8 -*-
# @Time    : 2019/3/28 16:31
# @Author  : 郭增祥
import sys
import os
from scrapy.cmdline import execute
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# execute(["scrapy","crawl","output.nsfc"])
execute(["scrapy","crawl","baike.baidu"])

# from scrapy import cmdline
# import time
# time_str=time.strftime("%Y-%m-%d-%M-%S",time.localtime(time.time()))
# cmdline.execute(("scrapy crawl output.nsfc -o "+time_str+".csv -t csv").split())