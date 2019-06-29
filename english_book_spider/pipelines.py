# -*- coding: utf-8 -*-

from scrapy.conf import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from english_book_spider.models import EnglishBook
from scrapy.exceptions import CloseSpider


class EnglishBookSpiderPipeline(object):
    # 用于数据库存储
    def __init__(self):
        # 连接数据库

        self.engine = create_engine(settings['SQLALCHEMY_DATABASE_URI'])
        self.Session = sessionmaker(bind=self.engine)
        self.Session.configure(bind=self.engine)
        self.session = self.Session()

    def process_item(self, item, spider):
        try:
            # 查重处理
            repetition = self.session.query(EnglishBook).filter_by(origin_url=item['origin_url']).first()
            # 重复
            if repetition is None:
                # 插入数据
                english_book = EnglishBook(title=item['title'],
                                           origin_url=item['origin_url'],
                                           pan_code=item['pan_code'],
                                           pan_url=item['pan_url'])
                self.session.add(english_book)
                # 提交sql语句
                self.session.commit()
                print(item['title'], '提交成功')
            else:
                print(item['title'], '爬过了')

        except Exception as error:
            # 出现错误时打印错误日志
            print(error)
            raise CloseSpider('爬虫出错了')
