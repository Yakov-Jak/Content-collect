# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pprint import pprint
from itemadapter import ItemAdapter
from pymongo import MongoClient

class JobparserPipeline:
    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)
        client.drop_database('vac_scrapy')
        self.mongobase = client.vac_scrapy

    def process_item(self, item, spider):
        # Обработка зарплаты на хедхантере
        if spider.name == 'hhru':
            salary = item.pop('salary')
            if salary[0].replace(' ', '') == 'от':
                if salary[2].replace(' ', '') == 'до':
                    item['smin'] = int(salary[1].replace("\xa0", ""))
                    item['smax'] = int(salary[3].replace("\xa0", ""))
                else:
                    item['smin'] = int(salary[1].replace("\xa0", ""))
                    item['smax'] = None
            else:
                if salary[0].replace(' ', '') == 'до':
                    item['smin'] = None
                    item['smax'] = int(salary[1].replace("\xa0", ""))
                else:
                    item['smin'] = None
                    item['smax'] = None
        # Обработка зарплаты на суперджоб
        elif spider.name == 'sjru':
            salary = item.pop('salary')
            if salary[0] == 'от':
                item['smin'] = int(salary[2].replace("\xa0", "").replace('руб.', ''))
                item['smax'] = None
            elif salary[0] == 'до':
                item['smin'] = None
                item['smax'] = int(salary[2].replace("\xa0", "").replace('руб.', ''))
            elif salary[0].replace("\xa0", "").isdigit():
                item['smin'] = int(salary[0].replace("\xa0", ""))
                item['smax'] = int(salary[1].replace("\xa0", ""))
            else:
                item['smin'] = None
                item['smax'] = None
        else:
            pass

        collection = self.mongobase[spider.name]
        collection.insert_one(item)

        return item
