import scrapy
from scrapy.crawler import CrawlerProcess

class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    
    def __init__(self, domain=None, num_pages=5, *args, **kwargs):
        self.domain = domain
        self.steps_remaining = num_pages

    def start_requests(self):
        yield scrapy.Request(url=self.domain, callback=self.parse)

    def parse(self, response):
        product_urls = response.css('div.s-search-results h2 > a').xpath('@href').getall()
        sponsored_prod_urls = response.css('div.s-search-results div[data-component-type="sp-sponsored-result"] h2 > a').xpath('@href').getall()
        
        final_urls = [response.urljoin(url) for url in product_urls if url not in sponsored_prod_urls]
        yield {
            'source_url': response.request.url,
            'num_of_urls': len(final_urls),
            'product_urls': final_urls
        }
        self.steps_remaining-=1
        if self.steps_remaining > 0:
            next_page = response.css('li.a-last a::attr("href")').get()
            if next_page is not None:
                yield response.follow(next_page, self.parse)

def start_crawling(domain, output_json_path, num_pages=5):
    process = CrawlerProcess(settings={
        #'FEED_FORMAT': 'json', 'FEED_URI': 'items.json',
        'ITEM_PIPELINES': { 'pipelines.ItemPipeline': 300 },
        'OUTPUT_JSON_PATH': output_json_path,
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
    })
    process.crawl(AmazonSpider, domain=domain, num_pages=num_pages)
    process.start()

if __name__ == '__main__':
    domain='https://www.amazon.in/s?i=computers&bbn=1375424031&rh=n%3A976392031%2Cn%3A976393031%2Cn%3A1375424031%2Cp_n_feature_thirteen_browse-bin%3A12598159031%7C12598161031%7C12598162031%7C12598163031%7C12598164031%7C12598165031'
    output_json_path = './product_urls.json'
    num_pages = 5
    start_crawling(domain, output_json_path, num_pages)