# -*- coding: utf-8 -*-
# @Time    : 2019/4/6 15:39
# @Author  : 郭增祥
# @File    : format-教师信息挖掘

import w3lib.html as w3

class format(object):
    @classmethod
    def normalizeTool(cls,html):
        '''
        :param html: 需要去掉html代码的str字符串
        :return: 去掉html代码的字符串
        '''
        removeHtml = w3.replace_escape_chars(w3.replace_entities(w3.remove_tags(html)), replace_by=" ")
        removeEscapeChars = " ".join(removeHtml.split())
        return removeEscapeChars

    @classmethod
    def getInfo(cls,response,xpath_info):
        '''
        :param response: 响应
        :param xpath_info: xpath规则
        :return: xpath 所对应的网页信息
        '''
        if xpath_info is '' or xpath_info is None:
            return ''
        try:
            return "".join( "".join(response.xpath(xpath_info).extract()).replace(" ","").strip().split())
        except Exception as e:
            print("getInfo",e)
            return ""

    @classmethod
    def is_alphabet(cls, str):
        '''
        :param str: 判断小写a到z 或A到Z 是否在当前字符串中
        :return: True or False
        '''
        import re
        return bool(re.search('[a-zA-Z]', str))