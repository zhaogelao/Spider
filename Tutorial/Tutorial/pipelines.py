# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import pymongo

#截取text<=50，
class TextPipeline(object):
    def __init__(self):
        self.limit =50

    def process_item(self, item, spider):
        print(spider.name)
        if item['text']:
            if len(item['text'])>self.limit:
                item['text'] = item['text'][:self.limit].rstrip()+'...'
            return item
        else:
            return DropItem('出现异常')

class MongoPipeline(object):

    def __init__(self,mongo_url,mongo_db):
        self.mongo_url=mongo_url
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_url=crawler.settings.get('MONGO_URL'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(host=self.mongo_url,port=27017)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        name = item.__class__.__name__
        self.db[name].insert(dict(item))
        return item






