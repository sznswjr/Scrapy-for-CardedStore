# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
from CardedStore.items import GoodItem, GoodUrlItem


class CardedstorePipeline:
    def open_spider(self, spider):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["tordata"]
        self.good_url = self.db['good_url_all']
        # self.seller_url = self.db['seller_url_all']
        self.good = self.db['market']
        # self.seller = self.db['seller']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, GoodUrlItem):
            if self.good_url.find({"good_url": dict(item)['good_url']}).count() == 0:
                self.good_url.insert(dict(item))
        if isinstance(item, GoodItem):
            self.good_url.update_one({"good_url": dict(item)['good_url']}, {"$set": {"good_flag": 1}})
            if self.good.find({"good_uri": dict(item)['good_uri']}).count() == 0:
                self.good.insert(dict(item))
            pass
        # return item
