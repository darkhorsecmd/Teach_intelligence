'''
@author  : 郭增祥
@contact : mister_gzx@163.com
@file    : ReadSchoolList.py
@time    : 2019/5/8 20:23
'''

import os
class ReadSchoolList(object):
    #调用以下方法，需要注意 School_list_data 目录下面是否有文件

    #硬编码path路径
    path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))+"\\School_list_data"

    @classmethod
    def getFileNameList(cls):
        '''
        :return:文件名列表
        '''
        list_file =[]
        dirs = os.listdir(path=ReadSchoolList.path)
        for dir in dirs:
            list_file.append(dir)
        return list_file

    @classmethod
    def getFileAllData(cls):
        '''
        :return:{'学校_学院名1':[url1,url2...],'学校_学院名2':[url1,url2...]}
        '''
        file_name_list = ReadSchoolList.getFileNameList()
        file_dict ={}
        for file in file_name_list:
            file_content_list = []
            for line in open(ReadSchoolList.path+"\\"+file):
                file_content_list.append(line.replace("\n",""))
            file_dict[file]=file_content_list
        return file_dict


if __name__ == '__main__':
    result = ReadSchoolList.getFileAllData()
    print(result)