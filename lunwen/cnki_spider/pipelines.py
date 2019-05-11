# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi

class CnkiSpiderPipeline(object):
    def process_item(self, item, spider):
        return item
class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool
    @classmethod
    def from_settings(cls, settings):  # 这个方法会在初始化的时候被scrapy调用
        db_params = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset="utf8",
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        db_pool = adbapi.ConnectionPool("MySQLdb", **db_params)
        return cls(db_pool)

    def process_item(self, item, spider):
        # 使用twisted 将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error)

    def handle_error(self, failure):
        # 处理异步插入异常
        print(failure)

    def Isexist(self,cursor,isexist):
        print(isexist)
        sql = "select * from science where MD5 = '{0}'".format(isexist)
        try:
            pd = cursor.execute(sql)
            if pd==0:
                return True  #如果一个都没有查询到，返回true
            else:
                return False
        except Exception as e:
            print("Isexit 错误：",e)
    def do_insert(self, cursor, item):
        insert_sql = '''
                        insert into science(url,MD5,article_name,quote_num,quoted_article_list_url,publish_time,
                        come_from_website_name,come_from_website_url,come_from_periodical,Include_author_name,DepartmentName,author_name_list,IsFirstAuthor,
                        abstract_Zh,kw_main,doi,deep_search_word)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    '''
        if self.Isexist(cursor=cursor,isexist=str(item["MD5"])):
            cursor.execute(insert_sql,
                               (
                                   item["url"], item["MD5"], item["article_name"], item["quote_num"],
                                   item["quoted_article_list_url"],
                                   item["publish_time"],item["come_from_website_name"], item["come_from_website_url"],
                                   item["come_from_periodical"], item["Include_author_name"],
                                   item["DepartmentName"], item["author_name_list"], item["IsFirstAuthor"], item["abstract_Zh"],item["kw_main"],item["doi"],item["deep_search_word"]))
        else:
            print(item['article_name'],"已经存在，取消插入数据")
