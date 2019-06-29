# -*- coding: utf-8 -*-
from scrapy.conf import settings
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text

Base = declarative_base()


class EnglishBook(Base):
    __tablename__ = 'english_book'
    id = Column(Integer, primary_key=True)
    title = Column(String(200), unique=True, nullable=False)
    origin_url = Column(Text)
    pan_code = Column(String(8))
    pan_url = Column(Text)

    def __repr__(self):
        return '<EnglishBook %r>' % self.title
