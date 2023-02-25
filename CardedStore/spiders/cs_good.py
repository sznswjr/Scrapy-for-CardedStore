import scrapy
import pymongo
from urllib.parse import urlparse
import hashlib
from CardedStore.items import GoodItem
import datetime


class CsGoodSpider(scrapy.Spider):
    name = 'cs_good'
    allowed_domains = [
        'cardedsjztm6kkxlkdfxbiyx2mpnho2ze7ttvdybeoiuwwnmhzdqgqyd.onion']
    start_urls = [
        'http://cardedsjztm6kkxlkdfxbiyx2mpnho2ze7ttvdybeoiuwwnmhzdqgqyd.onion/product/samsung-galaxy-note10plus/']

    def parse(self, response):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["tordata"]
        self.good_url = self.db['good_url_all']

        for url_item in self.good_url.find({"good_flag": 0}):
            url = url_item["good_url"]
            yield scrapy.Request(url, callback=self.parse_good)

    def parse_good(self, response):
        name = response.xpath(
            '//h1[@class="product_title entry-title"]/text()').extract_first()
        print(name)
        url = response.url
        urlpar = urlparse(response.url)
        uri = urlpar.path[1:]

        # 提取价格，需分情况
        if len(response.xpath('//p[@class="price"]/span')) == 2:
            price = response.xpath('//p[@class="price"]/span/bdi/span/text()')[0].extract() \
                + response.xpath('//p[@class="price"]/span/bdi/text()')[0].extract() \
                + '-' \
                + response.xpath('//p[@class="price"]/span/bdi/span/text()')[1].extract() \
                + response.xpath('//p[@class="price"]/span/bdi/text()')[1].extract()
        elif len(response.xpath('//p[@class="price"]/ins')) > 0:
            price = response.xpath('//p[@class="price"]/ins/span/bdi/span/text()').extract_first() \
                + response.xpath('//p[@class="price"]/ins/span/bdi/text()').extract_first()
        else:
            price = response.xpath('//p[@class="price"]/span/bdi/span/text()')[0].extract() \
                + response.xpath('//p[@class="price"]/span/bdi/text()')[0].extract()

        cat = response.xpath(
            '//span[@class="posted_in"]/a/text()').extract_first()

        # todo
        detail = self.handle_description(response)

        image = response.xpath('//a[@class="fresco"]/@href').extract_first()

        time = datetime.datetime.now()

        # 保存图片
        yield scrapy.Request(image, callback=self.parse_handleimage)

        # print(name)
        # print(uri)
        # print(price)
        # print(cat)
        # print(detail)
        # print(image)
        item = GoodItem()
        item['good_name'] = name
        item['good_url'] = response.url
        item['good_uri'] = uri
        item['good_price'] = price
        item['good_seller'] = None
        item['good_seller_url'] = None
        item['good_cat'] = cat
        item['good_solds'] = -1
        item['good_ptime'] = None
        item['good_detail'] = detail
        item['good_image'] = image
        item['market_name'] = "CardedStore"
        item['crawl_date'] = time
        item['sort_time'] = time
        yield item

    def parse_handleimage(self, response):
        image_data = response.body
        hash_md5 = hashlib.md5()
        hash_md5.update(image_data)
        image_md5 = hash_md5.hexdigest()
        with open("./good_images/CardedStore/" + image_md5 + ".png", "wb+") as f:
            f.write(image_data)

    def handle_description(self, response):
        if len(response.xpath('//div[@id="tab-description"]/h1')) > 0:
            detail = response.xpath('//div[@id="tab-description"]/h1/text()').extract_first() + '\n' \
                + response.xpath('//div[@id="tab-description"]/p/text()').extract_first()
        elif len(response.xpath('//p[@class="c-head_dek"]')) > 0:
            detail = response.xpath(
                '//p[@class="c-head_dek"]/text()').extract_first()
        elif len(response.xpath('//div[@id="tab-description"]/div/div')) > 0:
            detail = response.xpath(
                '//div[@id="tab-description"]/div/div/text()').extract_first()
        elif len(response.xpath('//div[@id="tab-description"]/p/b')) > 0:
            detail = response.xpath('//div[@id="tab-description"]/p/text()').extract()[0] \
                + response.xpath('//div[@id="tab-description"]/p/b/text()').extract_first() \
                + response.xpath('//div[@id="tab-description"]/p/text()').extract()[1]
        elif len(response.xpath('//div[@id="tab-description"]/p/strong/text()')) > 0:
            detail = response.xpath('//div[@id="tab-description"]/p/strong/text()').extract_first() \
                + response.xpath('//div[@id="tab-description"]/p/text()').extract_first()
        else:
            detail = response.xpath(
                '//div[@id="tab-description"]/p/text()').extract_first()
        return detail
