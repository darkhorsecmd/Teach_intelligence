# -*- coding: utf-8 -*-
# @Time    : 2019/4/11 13:55
# @Author  : 郭增祥
# @File    : test_Content_Length-教师信息挖掘

import json
payload = {"ratifyNo": "", "projectName": "", "personInCharge": "", "dependUnit": "", "code": "",
           "projectType": "", "subPType": "", "psPType": "", "keywords": "", "ratifyYear": "",
           "conclusionYear": "", "beginYear": "", "endYear": "", "checkDep": "",
           "checkType": "",
           "quickQueryInput": "", "adminID": "", "pageNum": 0, "pageSize": 5, "queryType": "input",
           "complete": "true"}
print(len(str(payload)))