# -*- coding: utf-8 -*-
# @Time    : 2019/4/16 17:57
# @Author  : 郭增祥
# @File    : startmain-知网信息挖掘
import sys
import os
from scrapy.cmdline import execute

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
print(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy","crawl","cnki"])
