# -*- coding: utf-8 -*-

from scrapy.conf import settings
import pymysql


class NewsSpiderPipeline(object):
    # 用于数据库存储
    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(
            host=settings['MYSQL_HOST'],
            port=3306,
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            use_unicode=True)

        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        print(item)
        try:
            # 查重处理
            self.cursor.execute(
                'select * from english_book where title = %s',
                item['title'])
            # 是否有重复数据
            repetition = self.cursor.fetchone()

            # 重复
            if repetition:
                update_sql = 'update english_book set origin_url = "%s", pan_code = "%s", pan_url = "%s" where title = "%s"' % (
                item['origin_url'], item['pan_code'], item['pan_url'], item['title'])
                print(update_sql)
                self.cursor.execute(update_sql)
                # pass

            else:
                # 插入数据
                instert_sql = 'insert into english_book(title, pan_code, pan_url, origin_url) values ("%s","%s","%s","%s")' % (
                item['title'], item['pan_code'], item['pan_url'], item['origin_url'])
                print(instert_sql)
                self.cursor.execute(instert_sql)

                # 提交sql语句
            self.connect.commit()

        except Exception as error:
            # 出现错误时打印错误日志
            print('——————————出错误了——————————————', error)
        return item
