# -*- coding: utf-8 -*-
# @Time    : 2019/4/18 23:29
# @Author  : 郭增祥
# @File    : transerPinyin-百度学术信息挖掘
from pypinyin import *
class transferPinyin():
    @classmethod
    def tranPinyin(cls,s):
        return_list =[]
        english_name_list = lazy_pinyin(s)
        s1=english_name_list[0]+' '
        for index in range(1,len(english_name_list)):
             s1 += english_name_list[index]
        return_list.append(s1)
        # 姓名倒序的拼音名字
        s2=''
        for index in range(1, len(english_name_list)):
             s2 += english_name_list[index]
        s2 += ' ' + english_name_list[0]
        return_list.append(s2)
        return return_list
if __name__ == '__main__':
    print(transferPinyin.tranPinyin("史晗"))