# -*- coding: utf-8 -*-

# Scrapy settings for people project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'people'

SPIDER_MODULES = ['people.spiders']
NEWSPIDER_MODULE = 'people.spiders'
ROBOTSTXT_OBEY = False
CONCURRENT_REQUESTS = 10
COOKIES_ENABLED = True
ITEM_PIPELINES = {
   'people.pipelines.PeoplePipeline': 300,
}

USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36"

LOG_LEVEL='ERROR'
DOWNLOADER_MIDDLEWARES = {
    'people.middlewares.SeleniumMiddleware': 200
}

CSV_FILE = "MorganLevis people.csv"