# -*- coding: utf-8 -*-
import scrapy
import datetime
import json
import re
from english_post_spider.items import NewsSpiderItem
from english_post_spider.pipelines import NewsSpiderPipeline


class NewsSpider(scrapy.Spider):
    name = 'salt_tiger'
    start_urls = ['https://salttiger.com/?s=javascript']
    start_page = 1
    news_pipeline = NewsSpiderPipeline()

    def start_requests(self):
        return [scrapy.FormRequest(url=self.start_urls[0], dont_filter=False, callback=self.parse)]

    def parse(self, response):
        news_list = response.xpath("//h1[@class='entry-title']")
        # print(news_list)
        for info_item in news_list:
            news_item = NewsSpiderItem()
            news_item['title'] = info_item.xpath(".//a/text()").extract_first()
            news_item['origin_url'] = info_item.xpath(".//a/@href").extract_first()
            yield scrapy.Request(news_item['origin_url'], meta={'item': news_item}, callback=self.detail_parse, dont_filter=True)
            # print(news_item)

        next_link = response.xpath("//a[@class='nextpostslink']/@href").extract_first()

        if next_link:
            yield scrapy.Request(next_link, callback=self.parse)

    def detail_parse(self, response):
        item = response.meta['item']
        item['pan_url'] = response.xpath("//div[contains(@class,'entry-content')]//strong/a/@href").extract()[1]
        content = ','.join(response.xpath("//div[contains(@class,'entry-content')]//strong/text()").extract())
        match_obj = re.search(r'^(提取码).*(：\w{4})\b', content, re.M|re.I)
        item['pan_code'] = ''

        if match_obj:
            print("提取码:", match_obj.group().split('：').pop().strip())
            item['pan_code'] = match_obj.group().split('：').pop().strip()
        else:
            print('没有提取码')

        yield item
        # print(item)
