'''
@author  : 郭增祥
@contact : mister_gzx@163.com
@file    : zhengze.py
@time    : 2019/5/8 20:48
'''
import re
class zhengze():

    @classmethod
    def preclean(cls,s):
        return  re.sub('<[^<]+?>', '', s).replace('\n', '').strip()

    @classmethod
    def getSchoolName(cls,s):
        '''
        :param s: 学校名_学院名
        :return:  学校名
        '''
        pattern = '.*(?=_)'
        result = re.search(pattern=pattern, string=s).group(0)
        if result is None:
            return ''
        else:
            return result

    @classmethod
    def getAcademy(cls, s):
        '''
        :param s: 学校名_学院名
        :return:  学院名
        '''
        pattern = '(?<=_).*'
        result = re.search(pattern=pattern, string=s).group(0)
        if result is None:
            return ''
        else:
            return result


    @classmethod
    def preclean(cls,s):
        return  re.sub('<[^<]+?>', '', s).replace('\n', '').strip()

    @classmethod
    def getEmail(cls, s):
        # demo:s=邮箱: ligang @ nju.edu.cn
        # return:[ligang@nju.edu.cn]
        pattern = '\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+(cn|com|edu|net)'
        # pattern = '^([A-Za-z0-9]*)@([A-Za-z0-9][-A-Za-z0-9]+\.)+(cn|com|edu|net)'
        result = re.search(pattern, s)
        # result = "".join(str(ss) for ss in result_list)
        if result is None:
            return ' '
        else:
            print(result.group(0))
            return result.group(0)


    @classmethod
    def getPhoneNum(cls, s):
        # demo:s=手机号码:  13951671420  混乱字符
        # return: [13951671420]
        phoneNumPattern = '(13|14|15|17|18|19)[0-9]{9}'
        result = re.search(phoneNumPattern, s)
        # result = "".join(str(s) for s in temp)
        if result is None:
            return ' '
        else:
            return result.group(0)

    @classmethod
    def getTelNum(cls, s):  # (+\d{2,3}[\s-]?)
        # demo:s= 办公号码：+86 025 89681397 asdf
        # return:"+86 025 89681397"
        s = zhengze.preclean(s)
        telPattern = '\d{4}[—-]\d{7,8}|\d{3}[—-]\d{8}|8\d{7}'
        temp = re.findall(telPattern, s)
        # 去重
        result = {}.fromkeys(temp).keys()
        result = '|'.join(str(ss + '\t') for ss in result)
        if result is None:
            return ' '
        else:
            return result

    @classmethod
    def getTitle(cls, s):
        # demo:s=    职称:  副教授,讲师开放咨询时间
        # return: 副教授讲师
        pattern = '(教授|副教授|讲师|助教)'
        result = ''.join(str(ss) for ss in re.findall(pattern, s))
        if result is None:
            return '未知'
        else:
            index1 = result.find('教授')
            index2 = result.find('副教授')

            if index1 != -1 & index2 == -1:
                return '教授'

            if index2 != -1 & index1 == -1:
                return '副教授'

            if index1 != -1 & index2 != -1:
                if index1 - index2 == 1:
                    return '副教授'
                else:
                    return '教授'

            if result.find('讲师') != -1:
                return '讲师'

            if result.find('助教') != -1:
                return '助教'
            return result

    @classmethod
    def getDegree(cls, s):
        # demo:s=    学历:
        # return:  学士|硕士|博士
        pattern = '(学士|硕士|博士)'
        result = ''.join(str(ss) for ss in re.findall(pattern, s))
        if '博士' in result:
            return '博士'
        elif '硕士' in result:
            return '硕士'
        elif '本科' in result:
            return '学士'
        else:
            return '未知'

    @classmethod
    def getEducation(cls, s):
        pattern = '(本科|研究生)'
        result = ''.join(str(ss) for ss in re.findall(pattern, s))
        if '研究生' in result:
            return '研究生'
        elif '本科' in result:
           return '本科'
        else:
            return '未知'

    @classmethod
    def getName(cls,s):
        pattern = '[\u4e00-\u9fa5]'
        result = ''.join(str(ss) for ss in re.findall(pattern,s))
        if result is None:
            return ' '
        else:
            return result

    @classmethod
    def getresearchAreas(cls, testSentence):
        # 暂时没有深层次测试，后面会补充
        result = re.findall("从事\w*研究。*", testSentence)
        # print(result)
        if len(result) == 0:
            result = re.findall("研究领域(主要)?涉及[:：]?\w*。*", testSentence)
            # print(result)
            if len(result) == 0:
                result = re.findall("研究[(方向)(领域)][:：为是]?[\w“”]*。?", testSentence)
                # print(result)
                if len(result) == 0:
                    result = re.findall("科研方向[:：为是]?\w*。?", testSentence)
                    # print(result)
                    if len(result) == 0:
                        result = re.findall("(研究[\w、]+[,，。])", testSentence)
                    # print(result)
        result = "".join(result)
        if result is None:
            return ''
        else:
            return result

    @classmethod
    def get_Info(cls, s, type):
        if (type=="xuexiao"):
            return zhengze.getSchoolName(s)
        if (type=="xueyuan"):
            return zhengze.getAcademy(s)
        if (type == "telnum"):
            return zhengze.getTelNum(s)
        elif (type == "title"):
            return zhengze.getTitle(s)
        elif (type == "email"):
            return zhengze.getEmail(s)
        elif (type == "phonenum"):
            return zhengze.getPhoneNum(s)
        elif (type == 'education'):
            return zhengze.getEducation(s)
        elif type == 'degree':
            return zhengze.getDegree(s)
        elif type == 'researchfield':
            return zhengze.getresearchAreas(s)
        elif type == 'name':
            return zhengze.getName(s)
        else:
            return "传入了错误的字符串或类"


if __name__ == '__main__':
    print(zhengze.get_Info("河海大学_计算机学院","xuexiao"))