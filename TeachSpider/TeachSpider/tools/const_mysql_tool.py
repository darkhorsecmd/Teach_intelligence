# -*- coding: utf-8 -*-
# @Time    : 2019/4/19 9:39
# @Author  : 郭增祥
# @File    : constTool-百度学术信息挖掘
import configparser
import MySQLdb
import MySQLdb.cursors
from MySQLdb.cursors import DictCursor
from DBUtils.PooledDB import PooledDB
import pymysql
from twisted.enterprise import adbapi
import os

class MysqlPool(object):
    #不适用Mysql5.8 以上版本，有连接池，入库和出库速度较快
    __pool = None
    def __init__(self,config_option):
        '''

        :param config_option:  config目录下的 *.ini 配置文件名字
        '''
        self._conn = MysqlPool.__getConn(config_option=config_option)
        self._cursor = self._conn.cursor()

    @staticmethod
    def __getConn(config_option):
        """
        @summary:静态方法，从连接池中取出连接
        @return: MysqlDB.connection
        """
        if MysqlPool.__pool is None:
            cf = configparser.ConfigParser()
            config_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + "\\config\\Mysql_config.ini"
            cf.read(config_path)
            mincached=2
            maxcached=5
            if cf.get(config_option, "mincached") is not None:
                mincached = int(cf.get(config_option, "mincached"))  # 最小连接数
            if cf.get(config_option, "maxcached") is not None:
                maxcached = int(cf.get(config_option, "maxcached"))  # 最小连接数
            db_params = dict(
                creator=MySQLdb,
                mincached =mincached,
                maxcached=maxcached,
                host=cf.get(config_option, "MYSQL_HOST"),
                db=cf.get(config_option, "MYSQL_DBNAME"),
                user=cf.get(config_option, "MYSQL_USER"),
                passwd=cf.get(config_option, "MYSQL_PASSWORD"),
                charset="utf8",
                use_unicode=True,
            )
            __pool = PooledDB(**db_params)
            return __pool.connection()

    def getAll(self,sql,param = None):
        """
        @summary: 执行查询，并取出所有结果集
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list(字典对象)/boolean 查询到的结果集
        """
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        if count > 0:
            result = self._cursor.fetchall()
        else:
            result = False
        return result

    def getOne(self, sql, param=None):
        """
        @summary: 执行查询，并取出第一条
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list/boolean 查询到的结果集
        """
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        if count > 0:
            result = self._cursor.fetchone()
        else:
            result = False
        return result

    def getMany(self, sql, num, param=None):
        """
        @summary: 执行查询，并取出num条结果
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param num:取得的结果条数
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list/boolean 查询到的结果集
        """
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        if count > 0:
            result = self._cursor.fetchmany(num)
        else:
            result = False
        return result

    def insertOne(self, sql, value):
        """
        @summary: 向数据表插入一条记录
        @param sql:要插入的ＳＱＬ格式
        @param value:要插入的记录数据tuple/list
        @return: insertId 受影响的行数
        """
        self._cursor.execute(sql, value)
        return self.__getInsertId()

    def insertMany(self, sql, values):
        """
        @summary: 向数据表插入多条记录
        @param sql:要插入的ＳＱＬ格式
        @param values:要插入的记录数据tuple(tuple)/list[list]
        @return: count 受影响的行数
        """
        count = self._cursor.executemany(sql, values)
        return count

    def __getInsertId(self):
        """
        获取当前连接最后一次插入操作生成的id,如果没有则为０
        """
        self._cursor.execute("SELECT @@IDENTITY AS id")
        result = self._cursor.fetchall()
        return result[0]['id']

    def __query(self, sql, param=None):
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        return count

    def update(self, sql, param=None):
        """
        @summary: 更新数据表记录
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)
        @param param: 要更新的  值 tuple/list
        @return: count 受影响的行数
        """
        return self.__query(sql, param)

    def delete(self, sql, param=None):
        """
        @summary: 删除数据表记录
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)
        @param param: 要删除的条件 值 tuple/list
        @return: count 受影响的行数
        """
        return self.__query(sql, param)

    def begin(self):
        """
        @summary: 开启事务
        """
        self._conn.autocommit(0)

    def end(self, option='commit'):
        """
        @summary: 结束事务
        """
        if option == 'commit':
            self._conn.commit()
        else:
            self._conn.rollback()

    def dispose(self, isEnd=1):
        """
        @summary: 释放连接池资源
        """
        if isEnd == 1:
            self.end('commit')
        else:
            self.end('rollback')
        self._cursor.close()
        self._conn.close()

class Mysql_8_tool(object):
    #兼容5.8 ， 没有连接池
    def __init__(self,config_option):
        self._conn= self.get_db_connection(config_option=config_option)
        self._cursor = self._conn.cursor()

    def get_db_connection(self,config_option):
        cf = configparser.ConfigParser()
        config_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + "\\config\\Mysql_config.ini"
        cf.read(config_path)
        host = cf.get(config_option, "MYSQL_HOST")
        db = cf.get(config_option, "MYSQL_DBNAME")
        user = cf.get(config_option, "MYSQL_USER")
        passwd = cf.get(config_option, "MYSQL_PASSWORD")
        charset = "utf8"

        dbcon=pymysql.Connect(host=host, port=3306, user=user, passwd=passwd, db=db,
                         charset=charset,use_unicode=True)
        return dbcon

    def getAll(self,sql,param = None):
        """
        @summary: 执行查询，并取出所有结果集
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list(字典对象)/boolean 查询到的结果集
        """
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        if count > 0:
            result = self._cursor.fetchall()
        else:
            result = False
        return result

    def getOne(self, sql, param=None):
        """
        @summary: 执行查询，并取出第一条
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list/boolean 查询到的结果集
        """
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        if count > 0:
            result = self._cursor.fetchone()
        else:
            result = False
        return result

    def getMany(self, sql, num, param=None):
        """
        @summary: 执行查询，并取出num条结果
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param num:取得的结果条数
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list/boolean 查询到的结果集
        """
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        if count > 0:
            result = self._cursor.fetchmany(num)
        else:
            result = False
        return result

    def insertOne(self, sql, value):
        """
        @summary: 向数据表插入一条记录
        @param sql:要插入的ＳＱＬ格式
        @param value:要插入的记录数据tuple/list
        @return: insertId 受影响的行数
        """
        self._cursor.execute(sql, value)
        return self.__getInsertId()

    def insertMany(self, sql, values):
        """
        @summary: 向数据表插入多条记录
        @param sql:要插入的ＳＱＬ格式
        @param values:要插入的记录数据tuple(tuple)/list[list]
        @return: count 受影响的行数
        """
        count = self._cursor.executemany(sql, values)
        return count

    def __getInsertId(self):
        """
        获取当前连接最后一次插入操作生成的id,如果没有则为０
        """
        self._cursor.execute("SELECT @@IDENTITY AS id")
        result = self._cursor.fetchall()
        return result[0]['id']

    def __query(self, sql, param=None):
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        return count

    def update(self, sql, param=None):
        """
        @summary: 更新数据表记录
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)
        @param param: 要更新的  值 tuple/list
        @return: count 受影响的行数
        """
        return self.__query(sql, param)

    def delete(self, sql, param=None):
        """
        @summary: 删除数据表记录
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)
        @param param: 要删除的条件 值 tuple/list
        @return: count 受影响的行数
        """
        return self.__query(sql, param)

    def begin(self):
        """
        @summary: 开启事务
        """
        self._conn.autocommit(0)

    def end(self, option='commit'):
        """
        @summary: 结束事务
        """
        if option == 'commit':
            self._conn.commit()
        else:
            self._conn.rollback()

    def dispose(self, isEnd=1):
        """
        @summary: 释放连接池资源
        """
        if isEnd == 1:
            self.end('commit')
        else:
            self.end('rollback')
        self._cursor.close()
        self._conn.close()

if __name__ == '__main__':
    pass
    # print(os.path.abspath(os.path.dirname(os.path.dirname(__file__)))+"\\config\\Mysql_config.ini")
    # config_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))+"\\config\\Mysql_config.ini"
    # print(config_path)
    # print("ok")
    # # sql = 'select * from %s LIMIT 10'
    # # consttool = MysqlTool(config_option='Deparment_config')
    # # print(consttool.getData(sql))
    # # print("ok")
    # #
    # # consttool2 = MysqlTool(config_option='Teach_config')
    # # sql2 = 'select * from %s LIMIT %s'
    # # s=consttool2.getData(sql2,[2])
    # # print(s)
    # # print("ok")
    # mysqls  =MysqlPool("Deparment_config")  #生成一个学校的数据库连接池
    # sql = "select * from researchinstitutioninfo  limit 5"
    # result = mysqls.getAll(sql=sql)  #得到全部
    # if result:
    #     print("get all")
    #     for row in result:
    #         print("%s\t%s"%(row[0],row[1]))
    # sql = "select * from researchinstitutioninfo"
    # result = mysqls.getMany(sql=sql,num=3) #得到部分
    # if result:
    #     print("get many")
    #     for row in result:
    #         print("%s\t%s"%(row[0],row[1]))
    # sql = "select * from researchinstitutioninfo"
    # result = mysqls.getOne(sql=sql)  #得到一个
    # if result:
    #     print("get one")
    #     print(result[3])
    #     # print(result[0][1])
    #     # for row in result:
    #     #     print("%s"%(row["SchoolNameZh"]))
    # print("数据库总数据量:",mysqls.getOne(sql="select count(*) from researchinstitutioninfo")[0])
    # mysqls.dispose()  #释放资源
    # print("ok")
    # test = Mysql_8_tool('Teach_config')
    # print(test.getOne('select * from researcher_basic_info'))
    # print("\n")
    # print(test.getMany('select * from researcher_basic_info',2))

    #
    # test2 =Mysql_8_tool('article_config')
    # try:
    #     print(test2.getOne('select * from science where url=%s',"http://ueshu.baidu.com/usercenter/paper/show?paperid=052aecc10b7465cf73942e80e375ce87&site=xueshu_se"))
    # except Exception as e:
    #     print(e)
