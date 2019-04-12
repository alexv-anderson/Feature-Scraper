# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# https://stackoverflow.com/questions/32743469/scrapy-python-multiple-item-classes-in-one-pipeline

import json
import re

from features.items import ContentItem

from scrapy.exceptions import DropItem

class FeaturePipeline(object):
    def __init__(self):
        with open("./config.json", "r") as f:
            self._json_data = json.load(f)

class FilterFeaturePipeline(FeaturePipeline):
    def __init__(self, pipeline_type):
        FeaturePipeline.__init__(self)
        self._pipeline_type = pipeline_type

    def process_item(self, item, spider):
        if isinstance(item, self._pipeline_type):
            self.on_item(item, spider)
        return item
    
    def on_item(self, item, spider):
        pass

class ContentPipeline(FilterFeaturePipeline):
    def __init__(self):
        FilterFeaturePipeline.__init__(self, ContentItem)

        self.feature_regex_data = {}
        for feature_name in self._json_data["content_features"]:
            feature = self._json_data["content_features"][feature_name]
            self.feature_regex_data[feature_name] = {
                "regex": feature["regex"],
                "mode": feature["mode"]
            }

    def on_item(self, item, spider):
        regex_data = self.feature_regex_data[item["feature_name"]]
        if regex_data is None:
            raise DropItem("No content regex data for %s" % item["feature_name"])

        if regex_data["mode"] is "match" and re.match(regex_data["regex"], item["content"]) is None:
            raise DropItem("Content did not MATCH regex for %s" % item["feature_name"])
        elif regex_data["mode"] is "search" and re.search(regex_data["regex"], item["content"]) is None:
            raise DropItem("Content SEARCH for %s was not successful" % item["feature_name"])

        

