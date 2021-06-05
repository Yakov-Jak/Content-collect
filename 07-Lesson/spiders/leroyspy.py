import scrapy
from scrapy.http import HtmlResponse
from Leroy.items import LeroyItem
from scrapy.loader import ItemLoader


class LeroyspySpider(scrapy.Spider):
    name = 'leroyspy'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, search):
        super(LeroyspySpider, self).__init__()
        self.start_urls = [f'https://voronezh.leroymerlin.ru/search/?q={search}&suggest=true']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-qa-pagination-item='right']/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        goods_links = response.xpath("//div[@data-qa-product]/a/@href").extract()
        for link in goods_links:
            yield response.follow(link, callback=self.parse_good)

    def parse_good(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroyItem(), response=response)

        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('photos', "//img[@slot='thumbs']/@src")
        loader.add_value('link', response.url)
        loader.add_xpath('price', "//span[@slot='price']/text()")
        loader.add_xpath('param', "//dl[@class='def-list']/div//text()")
        yield loader.load_item()