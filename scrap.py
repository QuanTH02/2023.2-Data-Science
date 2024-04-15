import scrapy
from scrapy import Request

class MySpider(scrapy.Spider):
    name = 'myspider'
    allowed_domains = ['boxofficemojo.com']
    start_urls = ['https://www.boxofficemojo.com/month/february/?grossesOption=calendarGrosses']

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, headers={'User-Agent': 'Mozilla/5.0'}, callback=self.parse)

    def parse(self, response):
        title = response.xpath('//title/text()').get()
        print("Tiêu đề trang web:", title)
