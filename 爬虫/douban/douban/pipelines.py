# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv
import logging
import os

from itemadapter import ItemAdapter

from douban.items import DoubanItem


class DoubanPipeline:
    def process_item(self, item, spider):
        return item


class Pipeline_ToCSV(object):

    def __init__(self):
        # csv文件的位置,无需事先创建
        store_file = os.path.dirname(__file__) + '/data/qtw.csv'
        # 打开(创建)文件
        self.file = open(store_file, 'a', encoding='utf8')
        # csv写法
        self.writer = csv.writer(self.file)

    def process_item(self, item, spider):
        if isinstance(item, DoubanItem):
            # 判断字段值不为空再写入文件
            if item['reviewer_content']:
                self.writer.writerow((item['parent'], item['data_cid'],
                                      item['reviewer_author'],
                                      item['title'],
                                      item['reviewer_content']))
        else:
            self.writer.writerow((item['userId'], item['comment']))

        return item

    def close_spider(self, spider):
        # 关闭爬虫时顺便将文件保存退出
        self.file.close()