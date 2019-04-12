# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class FeatureItem(scrapy.Item):
    feature_type = scrapy.Field()

class ContentItem(FeatureItem):
    feature_name = scrapy.Field()
    tag = scrapy.Field()
    content = scrapy.Field()

class CustomItem(FeatureItem):
    feature_name = scrapy.Field()
    content = scrapy.Field()