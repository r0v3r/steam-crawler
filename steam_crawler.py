import scrapy

class SteamCrawler(scrapy.Spider):
    name = 'steamcrawler'
    start_urls = ['http://store.steampowered.com/search/?page=1']

    def parse(self, response):
        for item in response.css('a.search_result_row'):
            yield {'game': item.css('span.title::text').extract_first(),\
            'img': item.css('div.search_capsule img::attr(src)').extract_first(),\
            'release': item.css('div.search_released::text').extract_first(),\
            'price': item.css('div.search_price').extract_first()}
       
        for next_page in response.css('a.pagebtn'):
            yield response.follow(next_page, self.parse)
