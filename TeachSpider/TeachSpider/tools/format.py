# -*- coding: utf-8 -*-
# @Time    : 2019/4/6 15:39
# @Author  : 郭增祥
# @File    : format-教师信息挖掘

import w3lib.html as w3
import hashlib
from pypinyin import *


class format(Exception):



    @classmethod
    def tranPinyin(cls, s):
        return_list = []
        english_name_list = lazy_pinyin(s)
        s1 = english_name_list[0] + ' '
        for index in range(1, len(english_name_list)):
            s1 += english_name_list[index]
        return_list.append(s1)
        # 姓名倒序的拼音名字
        s2 = ''
        for index in range(1, len(english_name_list)):
            s2 += english_name_list[index]
        s2 += ' ' + english_name_list[0]
        return_list.append(s2)
        return return_list

    @classmethod
    def getMd5(cls,s):
        try:
            if(type(s) is not type("")):
                raise format()
            try:
                m2 = hashlib.md5()
                m2.update(s.encode("utf-8"))
                return m2.hexdigest()
            except Exception as he:
                print("he",he)
                return None
        except format as e:
            print("传入的待加密的MD5字符串不是str类型")
            return None

    @classmethod
    def normalizeTool(cls,html):
        '''
        :param html: 需要去掉html代码的str字符串
        :return: 去掉html代码的字符串
        '''
        removeHtml = w3.replace_escape_chars(w3.replace_entities(w3.remove_tags(html)), replace_by=" ")
        # removeHtml = w3.replace_escape_chars(w3.replace_entities(w3.remove_tags(html)))
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
if __name__ == '__main__':
    print(format.getMd5("hello"))