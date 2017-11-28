import scrapy
from price_parser import PriceParser
class SteamCrawler(scrapy.Spider):
    name = 'steamcrawler'
    start_urls = ['http://store.steampowered.com/search/?page=1']
    page = 1

    def parse(self, response):
        parser = PriceParser()

        for item in response.css('a.search_result_row'):
            parser.init()
            parser.feed(item.css('div.search_price').extract_first())
            
            yield {'game': item.css('span.title::text').extract_first(),\
            'appid': item.css('a::attr(data-ds-appid)').extract_first(),\
            'img': item.css('div.search_capsule img::attr(src)').extract_first(),\
            'release': item.css('div.search_released::text').extract_first(),\
            'price': parser.price}
        
        for next_page in response.css('a.pagebtn'):
            # print 'crawling next page'
            yield response.follow(next_page, self.parse)
