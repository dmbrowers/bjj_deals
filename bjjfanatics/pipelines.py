# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging
import sqlite3
from datetime import date

deal_date = date.today()


class SQLlitePipeline(object):

    def open_spider(self, spider):
        self.connection = sqlite3.connect("bjjfanatics.db")
        self.c = self.connection.cursor()
        try:
            self.c.execute('''
                CREATE TABLE deals(
                    date TEXT,
                    product TEXT,
                    link TEXT,
                    original_price TEXT,
                    discounted_price TEXT,
                    discount TEXT,
                    image_url TEXT
                )
            ''')
            self.connection.commit()
        except sqlite3.OperationalError:
            pass

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.c.execute('''
            INSERT INTO deals (date, product, link, original_price, discounted_price, discount, image_url) VALUES(?,?,?,?,?,?,?)
        ''', (
            deal_date,
            item.get('product'),
            item.get('link'),
            item.get('original_price'),
            item.get('discounted_price'),
            item.get('discount'),
            item.get('image_url')
        ))
        self.connection.commit()
        return item
