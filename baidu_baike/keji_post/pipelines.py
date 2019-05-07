# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
import scrapy
from scrapy.exceptions import DropItem
import MySQLdb
import MySQLdb.cursors

class KejiPostPipeline(object):
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

    def do_insert(self, cursor, item):
        insert_sql = '''
        insert into ResearchInstitutionInfo(SchoolNum,SchoolNameZh,SchoolNameEn,SchoolIntroduction,Schoolgrade,Province,
                City,Administration,SchoolLevel,private,IntroductionUrl,IntroductionContent,SpiderTime,
                Note2)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            '''
        cursor.execute(insert_sql,
                           (
                               item["SchoolNum"], item["SchoolNameZh"], item["SchoolNameEn"], item["SchoolIntroduction"],
                               item["Schoolgrade"],
                               item["Province"],item["City"], item["Administration"],
                               item["SchoolLevel"], item["private"],
                               item["IntroductionUrl"], item["IntroductionContent"], item["SpiderTime"], item["Note2"]))