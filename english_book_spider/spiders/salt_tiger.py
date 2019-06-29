# -*- coding: utf-8 -*-
import scrapy
import datetime
import json
import re
from english_book_spider.items import EnglishBookSpiderItem
from english_book_spider.pipelines import EnglishBookSpiderPipeline
from english_book_spider.models import EnglishBook


class EnglishBookSpider(scrapy.Spider):
    name = 'english_book_spider'
    start_urls = ['https://salttiger.com/?s=javascript']
    start_page = 1
    book_pipeline = EnglishBookSpiderPipeline()

    def start_requests(self):
        return [scrapy.FormRequest(url=self.start_urls[0], dont_filter=False, callback=self.parse)]

    # 获取列表
    def parse(self, response):
        news_list = response.xpath("//h1[@class='entry-title']")
        for info_item in news_list:
            book_item = EnglishBookSpiderItem()
            book_item['origin_url'] = info_item.xpath("a/@href").extract_first()
            repetition = self.book_pipeline.session.query(EnglishBook).filter_by(origin_url=book_item['origin_url']).first()    
            if repetition:
                continue
            book_item['title'] = info_item.xpath("a/text()").extract_first()
            yield scrapy.Request(book_item['origin_url'], meta={'item': book_item}, callback=self.detail_parse, dont_filter=True)

        next_link = response.xpath("//a[@class='nextpostslink']/@href").extract_first()

        if next_link:
            yield scrapy.Request(next_link, callback=self.parse)

    # 获取书的详情
    @staticmethod
    def detail_parse(response):
        item = response.meta['item']
        item['pan_url'] = response.xpath("//div[contains(@class,'entry-content')]//strong/a/@href").extract_first()
        if item['pan_url'] is None:
            item['pan_url'] = ','.join(response.xpath("//div[contains(@class,'entry-content')]//a/@href").extract())
        content = ','.join(response.xpath("//div[contains(@class,'entry-content')]//strong/text()").extract())
        match_obj = re.search(r'^(提取码).*(：\w{4})\b', content, re.M | re.I)
        item['pan_code'] = ''

        if match_obj:
            print("提取码:", match_obj.group().split('：').pop().strip())
            item['pan_code'] = match_obj.group().split('：').pop().strip()
        else:
            print('没有提取码')

        yield item
