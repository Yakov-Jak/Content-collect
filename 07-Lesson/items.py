# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst

# Кооректируем ссылку для скачивания файла хорошего качества.
def change_pict(value):
    try:
        result = value.replace('82', '1200')
        return result
    except Exception:
        return value

# Правильно ли здесь преобразовывать цену в ИНТ или лучше в паплайне?
# def price_mod(value):
#     try:
#         result = int(value['price'][0].replace(' ', ''))
#         return result
#     except Exception:
#         return value


class LeroyItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(change_pict))
    link = scrapy.Field(output_processor=TakeFirst())
    param = scrapy.Field()
    price = scrapy.Field(output_processor=TakeFirst())
    _id = scrapy.Field() # Нужно указать переменную для наполнения БД


