# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import logging
import re

from features.items import ContentItem

from scrapy.exceptions import DropItem

class FeaturePipeline(object):
    """Parent of all pipelines which work on features"""
    def __init__(self):
        """Load the configuration data so children can access filtering data"""
        with open("./config.json", "r") as f:
            self._json_data = json.load(f)

class SingleFeaturePipeline(FeaturePipeline):
    """Parent of all feature pipelines which only know how to operate on one type of item"""

    def __init__(self, pipeline_type):
        """
        Parameters:
        -----------
        pipeline_type
            The item which the pipeline can process. Will be passed a parameter to isinstance
        """
        FeaturePipeline.__init__(self)
        self._pipeline_type = pipeline_type

    def process_item(self, item, spider):
        """
        Parameters:
        -----------
        item
            See Scrapy documentation
        spider
            See Scrapy documentation
        """

        # https://stackoverflow.com/questions/32743469/scrapy-python-multiple-item-classes-in-one-pipeline
        if isinstance(item, self._pipeline_type):
            self.on_item(item, spider)
        return item
    
    def on_item(self, item, spider):
        """
        Eventhandler which is called when this pipeline is given an item which matches the instance given
        at the creation of this pipeline.

        Parameters:
        -----------
        item
            See Scrapy documentation
        spider
            See Scrapy documentation
        """
        pass

class ContentPipeline(SingleFeaturePipeline):
    def __init__(self):
        SingleFeaturePipeline.__init__(self, ContentItem)

        # Build data needed for each feature's regular expression
        self.feature_regex_data = {}
        for feature_name in self._json_data["content_features"]:
            feature = self._json_data["content_features"][feature_name]
            self.feature_regex_data[feature_name] = {
                "regex": feature["regex"],
                "mode": feature["mode"]
            }

    def on_item(self, item, spider):
        feature_name = item["feature_name"]
        # Load regular expression data for the feature which created this item
        regex_data = self.feature_regex_data[feature_name]

        # If this feature has no regulare expression data, then throw the data out.
        # TODO: Should we keep doing this?
        if regex_data is None:
            message = "ContentPipeline dropped a %s because the %s content feature has not regex data." % self._pipeline_type, feature_name
            logging.log(logging.WARNING, message)
            raise DropItem(message)

        # If the regular expression is a valid mode and doesn't match, then throw the data out.
        if "mode" in regex_data and regex_data["mode"] in ["match", "search"]:
            logging.log(logging.WARNING, "Mode = %s" % regex_data["mode"])
            if regex_data["mode"] == "match" and re.match(regex_data["regex"], item["content"]) is None:
                raise DropItem("Content did not MATCH regex for %s" % item["feature_name"])
            elif regex_data["mode"] == "search" and re.search(regex_data["regex"], item["content"]) is None:
                raise DropItem("Content SEARCH for %s was not successful" % item["feature_name"])
        else:
            message = "ContentPipeline dropped a %s because the %s content feature has an incorrect mode. Expected either 'match' or 'search'." % self._pipeline_type, feature_name
            logging.log(logging.WARNING, message)
            raise DropItem(message)

        

