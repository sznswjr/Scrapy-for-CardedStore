# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CardedstoreItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class GoodUrlItem(scrapy.Item):
    good_url = scrapy.Field()
    good_flag = scrapy.Field()
    market_name = scrapy.Field()

class GoodItem(scrapy.Item):
    good_name = scrapy.Field()
    good_url = scrapy.Field()
    good_uri = scrapy.Field()
    good_price = scrapy.Field()
    good_seller = scrapy.Field()
    good_seller_url = scrapy.Field()
    good_cat = scrapy.Field()
    good_solds = scrapy.Field()
    good_ptime = scrapy.Field()
    good_detail = scrapy.Field()
    good_image = scrapy.Field()
    market_name = scrapy.Field()
    crawl_date = scrapy.Field()
    sort_time = scrapy.Field()
