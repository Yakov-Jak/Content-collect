# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from pymongo import MongoClient


class InstaparsPipeline:
    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)
        client.drop_database('insta_db')
        self.mongobase = client.insta_db


    def process_item(self, item, spider):
        if item['type'] == 'post':
            collection = self.mongobase[item['username']]
            collection.insert_one(item)
        elif item['type'] == 'flwrs':
            collection = self.mongobase['Flwrs_'+item['group']]
            collection.insert_one(item)
        else:
            collection = self.mongobase['Flwng_'+item['group']]
            collection.insert_one(item)
        return item
