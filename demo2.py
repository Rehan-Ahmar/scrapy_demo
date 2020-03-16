import scrapy
from scrapy.crawler import CrawlerProcess

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'https://www.amazon.in/s?i=computers&bbn=1375424031&rh=n%3A976392031%2Cn%3A976393031%2Cn%3A1375424031%2Cp_n_feature_thirteen_browse-bin%3A12598159031%7C12598161031%7C12598162031%7C12598163031%7C12598164031%7C12598165031',
    ]

    def parse(self, response):
        product_urls = response.css('div.s-search-results h2 > a').xpath('@href').getall()
        sponsored_prod_urls = response.css('div.s-search-results div[data-component-type="sp-sponsored-result"] h2 > a').xpath('@href').getall()
        
        final_urls = [response.urljoin(url) for url in product_urls if url not in sponsored_prod_urls]
        print('***************************************')
        print(final_urls)
        print(len(final_urls))
        print('***************************************')
        
        for quote in response.css('span.SEARCH_RESULTS-SEARCH_RESULTS'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.xpath('span/small/text()').get(),
            }

        '''next_page = response.css('li.next a::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)'''


process = CrawlerProcess(settings={
    'FEED_FORMAT': 'json',
    'FEED_URI': 'items.json',
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
})

process.crawl(QuotesSpider)
process.start() 