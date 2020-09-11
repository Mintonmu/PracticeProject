# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    parent = scrapy.Field()
    reviewer_author = scrapy.Field()
    title = scrapy.Field()
    data_cid = scrapy.Field()
    reviewer_content = scrapy.Field()

class YoukuItem(scrapy.Item):
    comment = scrapy.Field()
    userId = scrapy.Field()