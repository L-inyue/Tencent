# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from .settings import *


class TencentPipeline(object):
    def open_spider(self,spider):
        self.mongo = pymongo.MongoClient(
            host=MANGO_HOST,
            port=MANGO_PORT,
        )
        self.db = self.mongo[MANGO_DB]
        self.myset = self.db[MANGO_SET]

    # def process_item(self, item, spider):
    #     with open('tencent.txt', 'a') as f:
    #         f.write(item['title'])
    #         f.write(item['duty'])
    #         f.write(item['yaoqiu'])
    #         f.write('\n')
    #         f.write('\n')
    #     print(item['title'], item['duty'], item['yaoqiu'])
    #     return item

    def process_item(self, item, spider):
        item_dict = dict(item)
        print(item_dict)
        self.myset.insert_one(item_dict)
        return item
