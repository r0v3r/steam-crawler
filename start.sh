# rm data/$(date -d "today" +"%Y%m%d").json

# scrapy runspider steam_crawler.py -o data/$(date -d "today" +"%Y%m%d").json

scrapy runspider steam_crawler.py