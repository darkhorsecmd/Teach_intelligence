# -*- coding: utf-8 -*-
# @Time    : 2019/4/6 15:39
# @Author  : 郭增祥
# @File    : format-教师信息挖掘
# @Pakage  :
class format(object):
    @classmethod
    def getInfo(cls,response,xpath_info):
        if xpath_info is '' or xpath_info is None:
            return ''
        return "".join("".join(response.xpath(xpath_info).extract()).replace(" ","").strip().split())