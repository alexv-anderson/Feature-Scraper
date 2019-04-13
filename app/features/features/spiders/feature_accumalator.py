import scrapy
import csv
import json
import logging

from features.items import ContentItem, CustomItem, PageGrabItem

class FeatureSpider(scrapy.Spider):
    name = "feature-spider"

    def __init__(self):
        scrapy.Spider.__init__(self)
        with open("./config.json", "r") as f:
            self._json_data = json.load(f)

    def start_requests(self):
        urls = []
        with open("./urls.csv", "r") as f:
            csv_reader = csv.DictReader(f)
            for row in csv_reader:
                urls.append(row["url"])
                
        for url in urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        for feature_name in self._json_data["content_features"]:
            content_feature = self._json_data["content_features"][feature_name]
            for selector in response.xpath('//{0}'.format(content_feature["tag"])):
                for content in selector.xpath("text()").getall():
                    yield ContentItem({
                        # "feature_type": "content",
                        "feature_name": feature_name,
                        "tag": content_feature["tag"],
                        "content": content
                    })

        for feature_name in self._json_data["custom_features"]:
            custom_feature = self._json_data["custom_features"][feature_name]
            for selector in response.xpath(custom_feature["xpath_expr"]):
                for selected in selector.getall():
                    yield CustomItem({
                        # "feature_type": "custom",
                        "feature_name": feature_name,
                        "content": selected
                    })
        
        if "enabled" in self._json_data["page_grab"] and self._json_data["page_grab"]["enabled"]:
            yield PageGrabItem({"response": response})
