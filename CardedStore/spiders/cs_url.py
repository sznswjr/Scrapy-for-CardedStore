import scrapy
import pymongo
from CardedStore.items import GoodUrlItem


class CsUrlSpider(scrapy.Spider):
    name = 'cs_url'
    allowed_domains = ['cardedsjztm6kkxlkdfxbiyx2mpnho2ze7ttvdybeoiuwwnmhzdqgqyd.onion']
    start_urls = ['http://cardedsjztm6kkxlkdfxbiyx2mpnho2ze7ttvdybeoiuwwnmhzdqgqyd.onion/']

    def parse(self, response):
        url_list = response.xpath('//li[@class="category_grid_item"]/div/a/@href').extract()
        for url in url_list:
            # name = a.xpath('./text()').extract()
            # print(name[0])
            # print(url)
            yield scrapy.Request(url, callback=self.parse_goodtype)

    def parse_goodtype(self, response):
        # print("hhh")
        url_list = response.xpath('//ul[@id="products"]/li/figure/div[@class="category-discription-grid"]/h4/a/@href').extract()
        for url in url_list:
            # name = a.xpath('./text()').extract()
            # print(name[0])
            # print(url)
            item = GoodUrlItem()
            item['good_url'] = url
            item['good_flag'] = 0
            item['market_name'] = "CardedStore"
            yield item
