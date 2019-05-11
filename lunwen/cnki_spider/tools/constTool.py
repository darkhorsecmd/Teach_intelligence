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

#功能比较少
class MysqlTool(object):
    def __init__(self,config_option):
        self.DBName=''
        self.db = self.dbFun(config_option=config_option)
    def do_query(self,cursor,sql,param = None):
        # 真正查询数据的地方
        print("do_query")
        # sql = 'select * from %s LIMIT %s'
        print(sql)
        try:
            if param is None:
                cursor.execute(sql %self.TBName)
            results = cursor.fetchall()
            if (results.__len__()) > 0 :
                return results
            else:
                return None
        except Exception as e:
            print(self.DBName+"查询数据失败,原因："+f"{e}")
        finally:
            cursor.close()
    def getData(self,sql,param =None):
        #提供外部接口
        # query = self.db.runInteraction(self.do_query)
        # query.addErrback(self.handle_error)
        try:
            self.con = self.db.connection()#以后每次需要数据库连接就是用connection（）函数获取连接就好了
            return self.do_query(self.con.cursor(),sql=sql,param=param)
        except Exception as e:
            print("getData():",e)
        finally:
            self.con.close()
    def dbFun(self,config_option):
        #创建连接
        cf = configparser.ConfigParser()
        cf.read("../config/Mysql_config.ini")
        print(cf.sections())
        self.DBName = cf.get(config_option,"MYSQL_HOST")
        self.TBName = cf.get(config_option,"MYSQL_TBNAME")
        db_params = dict(
            creator=MySQLdb,
            host=cf.get(config_option, "MYSQL_HOST"),
            db=cf.get(config_option, "MYSQL_DBNAME"),
            user=cf.get(config_option, "MYSQL_USER"),
            passwd=cf.get(config_option, "MYSQL_PASSWORD"),
            charset="utf8",
            use_unicode=True,
        )
        db = PooledDB(**db_params)
        return db

        #下面注释部分是无连接池使用方法
        # db_params = dict(
        #     host=cf.get(config_option, "MYSQL_HOST"),
        #     port=3306,
        #     db=cf.get(config_option, "MYSQL_DBNAME"),
        #     user=cf.get(config_option, "MYSQL_USER"),
        #     passwd=cf.get(config_option, "MYSQL_PASSWORD"),
        #     charset="utf8",
        #     use_unicode=True,
        # )
        # db=pymysql.Connect(**db_params)
        # return db


#第二个赶紧会更好用
class MysqlPool(object):
    __pool = None
    def __init__(self,config_option):
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
            db_params = dict(
                creator=MySQLdb,
                mincached = int(cf.get(config_option, "mincached")),  #最小连接数
                maxcached = int(cf.get(config_option, "maxcached")),  #最大连接数
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

if __name__ == '__main__':
    print(os.path.abspath(os.path.dirname(os.path.dirname(__file__)))+"\\config\\Mysql_config.ini")
    config_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))+"\\config\\Mysql_config.ini"
    print(config_path)
    print("ok")
    # sql = 'select * from %s LIMIT 10'
    # consttool = MysqlTool(config_option='Deparment_config')
    # print(consttool.getData(sql))
    # print("ok")
    #
    # consttool2 = MysqlTool(config_option='Teach_config')
    # sql2 = 'select * from %s LIMIT %s'
    # s=consttool2.getData(sql2,[2])
    # print(s)
    # print("ok")
    mysqls  =MysqlPool("Deparment_config")  #生成一个学校的数据库连接池
    sql = "select * from researchinstitutioninfo  limit 5"
    result = mysqls.getAll(sql=sql)  #得到全部
    if result:
        print("get all")
        for row in result:
            print("%s\t%s"%(row[0],row[1]))
    sql = "select * from researchinstitutioninfo"
    result = mysqls.getMany(sql=sql,num=3) #得到部分
    if result:
        print("get many")
        for row in result:
            print("%s\t%s"%(row[0],row[1]))
    sql = "select * from researchinstitutioninfo"
    result = mysqls.getOne(sql=sql)  #得到一个
    if result:
        print("get one")
        print(result[3])
        # print(result[0][1])
        # for row in result:
        #     print("%s"%(row["SchoolNameZh"]))
    print("数据库总数据量:",mysqls.getOne(sql="select count(*) from researchinstitutioninfo")[0])

    mysqls.dispose()  #释放资源
    print("ok")
