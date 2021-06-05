# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient

# Функция обработки Характеристик товара. Выбираем только текстовые значения.
# Первая текстовая строка - наименование характеристики. Запоминается как ключи
# Вторая текстовая строка - значение характеристики.
# Далее по ключу и значению формируется словарь.

def param_clear(param_list):
    param_dict = {}
    i = 0
    for el in param_list:
        el = el.replace('  ', '').replace('\n', '')
        if el != '':
            if i == 0:
                p_key = el
                i = 1
            else:
                param_dict[p_key] = el
                i = 0
        else:
            pass
    return param_dict


class LeroyPipeline:
    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)
        client.drop_database('leroy_goods')
        leroy_goods = client.leroy_goods
        self.collection = leroy_goods.search # Создаём коллекцию

    def process_item(self, item, spider):
        param = param_clear(item['param'])
        item['param'] = param
        item['price'] = int(item['price'].replace(' ', ''))
        self.collection.insert_one(item)
        print()
        return item


class LeroyPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except TypeError as e:
                    print(e)

    # Метод класса ImagesPipeline для реализации привязки ссылки фото к ITEM'у
    # В info содержится информация о загружаемых файлах.
    # results - список кортежей со словарями, в которых содержится информация по каждому файлу. К чему он привязан.
    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
            # Если в results первый элемент - True, то заменяем список ссылок на файлы
            # списком словарей с данными о файлах
        return item