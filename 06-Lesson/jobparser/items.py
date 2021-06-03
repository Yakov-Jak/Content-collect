# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HhruItem(scrapy.Item):
    name = scrapy.Field()
    salary = scrapy.Field()
    smin = scrapy.Field()
    smax = scrapy.Field()
    link = scrapy.Field()
    _id = scrapy.Field()


class SjruItem(scrapy.Item):
    name = scrapy.Field()
    salary = scrapy.Field()
    smin = scrapy.Field()
    smax = scrapy.Field()
    link = scrapy.Field()
    _id = scrapy.Field()