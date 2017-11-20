import scrapy

class SteamCrawler(scrapy.Spider):
    name = 'steamcrawler'
    start_urls = ['http://store.steampowered.com/search/?filter=topsellers&page=1']

    def parse(self, response):
        for item in response.css('a.search_result_row'):
            # yield {'name': item.css('span.title ::text').extract_first(), 'price': item.css('div.search_price ::text')}
            yield {'game': item.css('span.title ::text').extract_first(), 'price': item.css('div.search_price ::text').extract_first()}
            # print {'title': title.css('a ::text').extract_first()}

        for next_page in response.css('a.pagebtn'):
            yield response.follow(next_page, self.parse)