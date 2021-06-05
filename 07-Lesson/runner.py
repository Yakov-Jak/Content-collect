from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from Leroy.spiders.leroyspy import LeroyspySpider
from Leroy import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    # query = input('')

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeroyspySpider, search='матрас')
    process.start()