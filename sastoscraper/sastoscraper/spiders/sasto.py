import scrapy
from ..items import SastoscraperItem as Item

class SastoSpider(scrapy.Spider):
    name = 'sasto'
    allowed_domains = ['www.sastodeal.com']
    start_urls = ['https://www.sastodeal.com/catalogsearch/result/index/?q=Fantech+headphones']

    def parse(self, response):
        item_links = list(set([link for link in response.css("div.product-item-info a::attr('href')") if link.get() != "#"]))
        for link in item_links:
            yield response.follow(link.get(), callback=self.parse_item)
    
    def parse_item(self, response):
        print(f"response.url")
        item = Item()
        # item['price'] = response.css("span.price").get()
        item['price'] = str(response.css("span.price-final_price span.price::text").get().replace("रू", "").strip())
        item['name'] = response.css("h1.page-title span::text").get().strip()
        # if response.css('span.stockqty span::text').get():
        #     item['availability'] = response.css('span.stockqty span::text').get().replace("\n", " ")
        # else:
        #     item['availability'] = "Not available"
        item['availability'] = response.css('span.stockqty span::text').get().replace("\n", " ")
        item['url'] = response.url
        yield item
