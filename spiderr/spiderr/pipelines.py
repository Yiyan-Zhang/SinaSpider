# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi

from spiderr.items import HotspotItem,CommentItem

global HotspotItem

class WeiboPipeline(object):
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)  # 调用插入的方法
        query.addErrback(self._handle_error, item, spider)  # 调用异常处理方法
        return item

    @classmethod
    def from_settings(cls, settings):
        '''1、@classmethod声明一个类方法，而对于平常我们见到的则叫做实例方法。
           2、类方法的第一个参数cls（class的缩写，指这个类本身），而实例方法的第一个参数是self，表示该类的一个实例
           3、可以通过类来调用，就像C.f()，相当于java中的静态方法'''
        dbparams = dict(
            host=settings['MYSQL_HOST'],  # 读取settings中的配置
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',  # 编码要加上，否则可能出现中文乱码问题
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=False,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparams)  # **表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
        return cls(dbpool)  # 相当于dbpool付给了这个类，self中可以得到

    def __init__(self, dbpool):
        self.dbpool = dbpool

    def _conditional_insert(self, tx, item):
        if isinstance(item, HotspotItem):
            sql = "INSERT INTO hotspot (title,mid1,replies,comments,likes,content,author_name) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            params = (item["title"], item["mid1"], item["replies"], item["comments"], item["likes"],item["content"], item["author_name"])
            tx.execute(sql, (params))
        elif isinstance(item, CommentItem):
            sql = "INSERT INTO comment (comment,mid2,comment_likes) VALUES (%s,%s,%s)"
            params = (item["comment"],item["mid2"],item["comment_likes"])
            tx.execute(sql, (params))

    def _handle_error(self, failue, item, spider):
        print failue