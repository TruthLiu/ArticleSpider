# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json

#将mysql数据库的操作变为异步操作
from twisted.enterprise import adbapi

import MySQLdb
import MySQLdb.cursors
from scrapy.pipelines.images import ImagesPipeline

from scrapy.exporters import JsonItemExporter

class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWithEncodingPipeline(object):
    #自定义json文件的导出
    def __init__(self):
        self.file=codecs.open("article.json","w",encoding="utf8")
    def process_item(self,item,spider):
        lines=json.dumps(dict(item),ensure_ascii=False)+"\n"
        self.file.write(lines)
        return item
    def spider_closed(self,spider):
        self.file.close()

#这种方式的插入数据库的速度比较慢，是同步的
class MysqlPipeline(object):
    def __init__(self):
        self.conn= MySQLdb.Connect('115.159.203.174','root','Llh9638527410.','scrapyspider1',3306,charset='utf8',use_unicode=True)
        self.cursor=self.conn.cursor()

    def process_item(self,item,spider):
        insert_sql="insert into" \
                   " jobbole_article(title,create_date,url,url_object_id,front_image_url,comment_nums,thumbup_nums,bookmark_nums,tags) " \
                   "values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        args=(item["title"],item["create_date"],item["url"],item["url_object_id"],item["front_image_url"][0],item["comment_nums"],item["thumbup_nums"],item["bookmark_nums"],item["tags"])
        self.cursor.execute(insert_sql,args)
        self.conn.commit()


#这种插入数据库的方式是异步的，使用数据库连接池
class MysqlTwistedPipline(object):
    def __init__(self,dbpool):
        self.dbpool=dbpool

    #链接数据库池
    @classmethod
    def from_settings(cls,settings):
        dbparms=dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True
        )
        dbpool=adbapi.ConnectionPool("MySQLdb",**dbparms)

        return cls(dbpool)


    #对数据库进行插入操作
    def process_item(self, item, spider):
        #使用twisted将mysql插入变量成异步执行
        query=self.dbpool.runInteraction(self.do_insert,item)
        query.addErrorback(self.handle_error)#处理异常

    def handle_error(self,failure):
        #处理异步插入的异常
        print(failure)


    def do_insert(self,cursor,item):
        #执行具体的插入
        insert_sql = "insert into" \
                     " jobbole_article(title,create_date,url,url_object_id,front_image_url,comment_nums,thumbup_nums,bookmark_nums,tags) " \
                     "values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        args = (item["title"], item["create_date"], item["url"], item["url_object_id"], item["front_image_url"][0],
                item["comment_nums"], item["thumbup_nums"], item["bookmark_nums"], item["tags"])
        cursor.execute(insert_sql, args)







class JsonExporterPipeline(object):
    #调用scrapy提供的json export导出json文件
    def __init__(self):
        #wb是二进制的方式打开
        self.file=open('articleexport.json','wb')
        self.exporter=JsonItemExporter(self.file,encoding='utf8',ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self,spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self,item,spider):
        self.exporter.export_item(item)
        return item







class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if "front_image_path" in item:
            for ok,value in results:
                image_file_path=value["path"]
            item["front_image_path"]=image_file_path

        return item

