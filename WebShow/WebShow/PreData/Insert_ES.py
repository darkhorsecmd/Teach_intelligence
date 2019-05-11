'''
@author  : 郭增祥
@contact : mister_gzx@163.com
@file    : Insert_ES.py
@time    : 2019/5/11 20:59
'''
import configparser
import os
from PreData.tools.constTool import MysqlPool as s_mysql


class Insert_Es(object):

    def __init__(self):
        # 读取配置文件设置
        self.mysql_config = configparser.ConfigParser()
        path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + "\\config\\Mysql_config.ini"

        self.mysql_config.read(path)

        # 生成数据库 连接池
        self.school_mysql = s_mysql("Deparment_config")
        self.teache_mysql = s_mysql("Teach_config")
        self.article_mysql = s_mysql("article_config")
        self.nsfc__mysql = s_mysql("nsfc_config")

        # 获取每个表的表名字
        self.school_TBName = self.mysql_config.get("Deparment_config", "MYSQL_TBNAME")
        self.teache_TBName = self.mysql_config.get("Teach_config", "MYSQL_TBNAME")
        self.article_TBName = self.mysql_config.get("article_config", "MYSQL_TBNAME")
        self.nsfc_TBName = self.mysql_config.get("nsfc_config", "MYSQL_TBNAME")

        # 预先构建一下 sql语句
        self.school_sql = "select * from " + self.school_TBName
        self.teache_sql = "select * from " + self.teache_TBName
        self.article_sql = "select * from " + self.article_TBName
        self.nsfc_sql = "select * from " + self.nsfc_TBName

    def Smain(self):
        school_datas = self.school_mysql.getAll(self.school_sql)
        if school_datas:
            for s_data in school_datas:
                sc_zh = str(s_data[2])  # 学校中文名
                sc_en = str(s_data[3])  # 学校英文名
                sc_name_list = []
                sc_name_list.append(sc_zh)
                sc_name_list.append(sc_en)
                teach_num = int(self.teache_mysql.getOne(
                    sql="select count(*) from " + self.teache_TBName + " where SchoolName1=\'" + sc_zh + "\'")[0])
                # 查询到的该学校教师个数是否大于0
                if teach_num > 0:
                    # 获取当前中文学校对应的所有教师数据
                    teach_datas = self.teache_mysql.getAll(sql=self.teache_sql + " where SchoolName1=\'" + sc_zh + "\'")
                    all_name_list = []  # 该学校所有教师存储list
                    for teach_data in teach_datas:
                        # 存储 中文名和英文名
                        per_teach_NameZh = teach_data[4]  # 中文名
                        per_teach_NameEn = teach_data[5]  # 英文正序

                        # 目前已经有了  学校中名sc_zh、学校英文名sc_en、教师中文名per_teach_NameZh、教师英文名per_teach_NameEn
                        # 单个学校数据  s_data
                        # 单个教师数据  teach_data
                        teach_name_list = []
                        teach_name_list.append(per_teach_NameZh)
                        teach_name_list.append(per_teach_NameEn)
                        Teach_per_lunwen_list  = self.GetDatas("lunwen",sc_name_list=sc_name_list,teach_name_list=teach_name_list)
                        Teach_per_xiangmu_list = self.GetDatas("xiangmu",sc_name_list=sc_name_list,teach_name_list=teach_name_list)

                        if Teach_per_lunwen_list is False:
                            Teach_per_lunwen_list = ''
                        if Teach_per_xiangmu_list is False:
                            Teach_per_xiangmu_list = ''
                        #融合 单个学校数据s_data && 单个教师数据teach_data &&单个教师论文数据 Teach_per_lunwen_list &&单个教师项目数据 Teach_per_xiangmu_list
                        self.preInsertEs()




    def GetDatas(self,tb_flag,sc_name_list,teach_name_list):
        '''
        :param tb_flag:     需要查询库的标识，论文库：lunwen  项目库:xiangmu
        :param sc_name:     学校中英文名字列表
        :param teach_name:  教师中英文名字列表
        :return:            该学校 && 教师 中文和英文 状态下的 论文数据或项目基金数据列表,没有数据返回False
        '''
        if tb_flag=='lunwen':
            # 中文学校名 && 中文教师名 -》》论文数据
                            # article_datas = self.article_mysql.getAll(
                            #     sql=self.article_sql + " where DepartmentName=\'" + sc_name + "\' and Include_author_name=\'" + teach_name + "\'")
            # 中文学校名 && 英文教师名 -》》论文数据

            # 英文学校名 && 英文教师名 -》》论文数据

            # 英文学校名 && 中文教师名 -》》论文数据

            pass
        elif tb_flag=='xiangmu':
            pass
        else:
            return False

    def preInsertEs(self):
        pass

if __name__ == '__main__':
    insert = Insert_Es()
    insert.Smain()
