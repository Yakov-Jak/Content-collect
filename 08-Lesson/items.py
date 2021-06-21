# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstaparsItem(scrapy.Item):
    # define the fields for your item here like:
    user_id = scrapy.Field()
    username = scrapy.Field()
    photo = scrapy.Field()
    likes = scrapy.Field()
    post = scrapy.Field()
    type = scrapy.Field()
    _id = scrapy.Field()


class InstaparsFollowers(scrapy.Item):
    # define the fields for your item here like:
    username = scrapy.Field()
    user_link = scrapy.Field()
    photo = scrapy.Field()
    group = scrapy.Field()
    type = scrapy.Field()
    _id = scrapy.Field()


class InstaparsFollowing(scrapy.Item):
    # define the fields for your item here like:
    username = scrapy.Field()
    user_link = scrapy.Field()
    photo = scrapy.Field()
    group = scrapy.Field()
    type = scrapy.Field()
    _id = scrapy.Field()