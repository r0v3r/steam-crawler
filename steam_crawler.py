import scrapy
from price_parser import PriceParser
import datetime
from pymongo import MongoClient

class SteamCrawler(scrapy.Spider):
    name = 'steamcrawler'
    start_urls = ['http://store.steampowered.com/search/?page=1']
    client = MongoClient('mongodb://localhost:27017')

    def parse(self, response):
        parser = PriceParser()
        db = self.client['steam-crawler']
        table = db['price']
        for item in response.css('a.search_result_row'):
            parser.init()
            parser.feed(item.css('div.search_price').extract_first())
            timestamp = datetime.datetime.now().strftime('%Y%m%d')
            table.insert({'game': item.css('span.title::text').extract_first(),\
            'timestamp': timestamp,\
            'appid': item.css('a::attr(data-ds-appid)').extract_first(),\
            'img': item.css('div.search_capsule img::attr(src)').extract_first(),\
            'release': item.css('div.search_released::text').extract_first(),\
            'price': parser.price})
            # yield {'game': item.css('span.title::text').extract_first(),\
            # 'timestamp': timestamp,\
            # 'appid': item.css('a::attr(data-ds-appid)').extract_first(),\
            # 'img': item.css('div.search_capsule img::attr(src)').extract_first(),\
            # 'release': item.css('div.search_released::text').extract_first(),\
            # 'price': parser.price}


        for next_page in response.css('a.pagebtn:last_child'):
            yield response.follow(next_page, self.parse)