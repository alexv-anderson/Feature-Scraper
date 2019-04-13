# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ContentItem(scrapy.Item):
    feature_name = scrapy.Field()
    tag = scrapy.Field()
    content = scrapy.Field()

class CustomItem(scrapy.Item):
    feature_name = scrapy.Field()
    content = scrapy.Field()

class PageGrabItem(scrapy.Item):
    response = scrapy.Field()