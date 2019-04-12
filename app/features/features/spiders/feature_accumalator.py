import scrapy
import csv
import json

from features.items import ContentItem

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
            for div in response.xpath('//{0}'.format(content_feature["tag"])):
                for content in div.xpath("text()").getall():
                    yield ContentItem({
                        "feature_name": feature_name,
                        "tag": content_feature["tag"],
                        "content": content
                    })
                # "content": div.xpath("text()").extract_first()
