# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsSpiderItem(scrapy.Item):
    title = scrapy.Field()
    origin_url = scrapy.Field()
    pan_code = scrapy.Field()
    pan_url = scrapy.Field()



