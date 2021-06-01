import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import HhruItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?L_save_area=true&clusters=true&enable_snippets=true&text=lean']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        vacancies_links = response.xpath("//a[@data-qa='vacancy-serp__vacancy-title']/@href").extract()
        for link in vacancies_links:
            yield response.follow(link, callback=self.vacancy_parse)


    def vacancy_parse(self, response: HtmlResponse):

        item_link = response.xpath("//link[@rel='canonical']/@href").extract_first()
        item_name = response.xpath("//h1/text()").extract_first()
        item_salary = response.xpath("//p/span[@data-qa='bloko-header-2']/text()").extract()
        if item_salary[0] == 'от':
            if item_salary[2] == 'до':
                item_smin = item_salary[1]
                item_smax = item_salary[3]
            else:
                item_smin = item_salary[1]
                item_smax = None
        else:
            if item_salary[0] == 'до':
                item_smin = None
                item_smax = item_salary[1]
            else:
                item_smin = None
                item_smax = None

        item = HhruItem(name=item_name, min_salary=item_smin, max_salary=item_smax, link=item_link)
        yield item
