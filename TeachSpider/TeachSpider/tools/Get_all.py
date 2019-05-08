'''
@author  : 郭增祥
@contact : mister_gzx@163.com
@file    : Get_all.py
@time    : 2019/5/8 21:09
'''
from tools.parese_a import parese_a
from tools.ReadSchoolList import ReadSchoolList as rd
from tools.chromes import NoProxy_Chrome as mychrome
class Get_all(object):

    def __init__(self,chrome=None):
        if chrome is None:
            self.chrome = mychrome().get_chrome()
        else:
            self.chrome = chrome

    def get_all(self,chrome=None):
        '''
        :param chrome: 需要传入一个浏览器对象
        :return: 学校_学院：教师列表(姓名，url)
        '''

        if chrome is None:
            chrome = self.chrome

        all_dict ={}
        xy = rd.getFileAllData()
        parse = parese_a(chrome=chrome)
        for School_Xueyuan_Name,Url_List in xy.items():
            Each_School_list = []
            for url in Url_List:
                # 每一个学校_学院存着对应的 教师列表
                ss = parse.set_url(url=url)
                for s in ss:
                    Each_School_list.append(s)
            all_dict[School_Xueyuan_Name.replace(".txt","")] = Each_School_list
        return all_dict

if __name__ == '__main__':
    # print(rd.getFileAllData())
    result = Get_all().get_all(chrome=mychrome().get_chrome())
    print(result)