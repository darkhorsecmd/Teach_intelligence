# -*- coding: utf-8 -*-
# @Time    : 2019/4/17 22:28
# @Author  : 郭增祥
# @File    : MD5-百度学术信息挖掘

import hashlib
class selfMd5(Exception):
    @classmethod
    def getMd5(cls,s):
        try:
            if(type(s) is not type("")):
                raise selfMd5()
            try:
                m2 = hashlib.md5()
                m2.update(s.encode("utf-8"))
                return m2.hexdigest()
            except Exception as he:
                print("he",he)
                return None
        except selfMd5 as e:
            print("传入的待加密的MD5字符串不是str类型")
            return None
if __name__ == '__main__':
    print(selfMd5.getMd5(12))

    s= "http://xueshu.baidu.com/usercenter/paper/show?paperid=56a398464307cb0ec95453f4f999497f&site=xueshu_se"
    print(type(s))
    print(selfMd5.getMd5(s))