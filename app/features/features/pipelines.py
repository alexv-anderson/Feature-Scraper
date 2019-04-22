# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import logging
import os
import re

from features.items import ContentItem, PageGrabItem

import scrapy

from scrapy.exceptions import DropItem, NotConfigured

class ConfigurablePipeline(object):
    """Parent of all pipelines which work on features"""
    def __init__(self):
        """Load the configuration data so children can access filtering data"""
        with open("./config.json", "r") as f:
            self._json_data = json.load(f)

    def _drop_and_log(self, pipeline_name, reason):
        message = "%s dropped a %s because the %s feature %s." % pipeline_name, self._pipeline_type, feature_name, reason
        logging.log(logging.WARNING, message)
        raise DropItem(message)

class SingleItemConfigurablePipeline(ConfigurablePipeline):
    """Parent of all feature pipelines which only know how to operate on one type of item"""

    def __init__(self, pipeline_type):
        """
        Parameters:
        -----------
        pipeline_type
            The item which the pipeline can process. Will be passed a parameter to isinstance
        """
        ConfigurablePipeline.__init__(self)
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

class ContentPipeline(SingleItemConfigurablePipeline):
    def __init__(self):
        SingleItemConfigurablePipeline.__init__(self, ContentItem)

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
            self._drop_and_log("ContentPipeline", "has not regex data")

        # If the regular expression is a valid mode and doesn't match, then throw the data out.
        if "mode" in regex_data and regex_data["mode"] in ["match", "search"]:
            if regex_data["mode"] == "match" and re.match(regex_data["regex"], item["content"]) is None:
                self._drop_and_log("ContentPipeline", "content did not MATCH regex %s" % item["regex"])
            elif regex_data["mode"] == "search" and re.search(regex_data["regex"], item["content"]) is None:
                self._drop_and_log("ContentPipeline", "content SEARCH could not find match for regex %s" % item["regex"])
        else:
            self._drop_and_log("ContentPipeline", "has an incorrect mode. Expected either 'match' or 'search'.")

class PageGrabPipeline(SingleItemConfigurablePipeline):
    def __init__(self):
        SingleItemConfigurablePipeline.__init__(self, PageGrabItem)

        self._output_dir_path = "./pageGrabOutput"
        if "enabled" in self._json_data["page_grab"] and self._json_data["page_grab"]["enabled"]:
            if "output_dir" in self._json_data["page_grab"]:
                self._output_dir_path = self._json_data["page_grab"]["output_dir"]
                if not os.path.exists(self._output_dir_path) or not os.path.isdir(self._output_dir_path):
                    logging.error("Path in 'output_dir' property the the 'page_grab' object is not a directory using default path of %s" % self._output_dir_path)
            else:
                logging.warn("No 'output_dir' property found for 'page_grab' using default path of %s" % self._output_dir_path)
            os.mkdir(self._output_dir_path)
        else:
            # https://docs.scrapy.org/en/latest/topics/exceptions.html#notconfigured
            message = "Page grabbing has been disabled"
            logging.info(message)
            raise NotConfigured(message)
        
        self._header_encoding = self._json_data["page_grab"]["header_encoding"]
        self._num_items_processed = 0

        
        
    def on_item(self, item, spider):
        item_output_dir_path = os.path.join(self._output_dir_path, '{:04d}'.format(self._num_items_processed))
        self._num_items_processed += 1
        os.mkdir(item_output_dir_path)
        
        response = item["response"]

        response_has_text = False
        response_extension = "byte"
        if isinstance(response, scrapy.http.TextResponse):
            response_has_text = True
            response_extension = "txt"
            if isinstance(response, scrapy.http.HtmlResponse):
                response_extension = "html"
            elif isinstance(response, scrapy.http.XmlResponse):
                response_extension = "xml"
        

        response_body_file_name = os.path.join(item_output_dir_path, "response_body.%s" % response_extension)
        # https://stackoverflow.com/questions/12092527/python-write-bytes-to-file
        with open(response_body_file_name, "w+" if response_has_text else "wb+") as f:
            if response_has_text:
                f.write(response.text)
            else:
                f.write(response.body)

        response_meta = {
            "http": {
                "response_url": response.url,
                "status": response.status,
                "headers": {}
            },
            "scrapy": {
                "flags": response.flags,
                "encoding": response.encoding if response_has_text else None,
                "request_meta": response.meta
            },
            "crawler": {
                "response_extension": response_extension,
                "response_has_text": response_has_text,
            }
        }

        self._populate_headers(response.headers, response_meta["http"]["headers"])
        
        with open(os.path.join(item_output_dir_path, "response_meta.json"), "w+") as f:
            json.dump(response_meta, f, indent=2)

        request = response.request
        request_meta = {
            "http": {
                "url": request.url,
                "method": request.method,
                "headers": {}
            },
            "scrapy": {
                "meta": request.meta
            }
        }
        self._populate_headers(request.headers, request_meta["http"]["headers"])
        with open(os.path.join(item_output_dir_path, "request_meta.json"), "w+") as f:
            json.dump(request_meta, f, indent=2)
    
    def _populate_headers(self, headers, d):
        for key in headers:
            # http://book.pythontips.com/en/latest/map_filter.html
            # https://stackoverflow.com/questions/31058055/how-do-i-convert-a-python-3-byte-string-variable-into-a-regular-string/31060836
            d[str(key, self._header_encoding)] = list(map(
                lambda byte_string: str(byte_string, self._header_encoding),
                headers.getlist(key)
            ))

