# -*- coding: utf-8 -*-


BOT_NAME = 'english_post_spider'

SPIDER_MODULES = ['english_post_spider.spiders']
NEWSPIDER_MODULE = 'english_post_spider.spiders'

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'

ROBOTSTXT_OBEY = False

DOWNLOAD_DELAY = 3

ITEM_PIPELINES = {
    'english_post_spider.pipelines.NewsSpiderPipeline': 3
}

HTTPCACHE_ENABLED = True
TELNETCONSOLE_ENABLED = False
CONCURRENT_REQUESTS = 1
CLOSESPIDER_ERRORCOUNT = 1

HTTPCACHE_EXPIRATION_SECS = 3600

MYSQL_HOST = '127.0.0.1'
MYSQL_DBNAME = 'book'
MYSQL_USER = 'root'
MYSQL_PASSWD = 'root'
