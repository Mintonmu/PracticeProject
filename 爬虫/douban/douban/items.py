# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    parent = scrapy.Field()
    level = scrapy.Field()
    data_cid = scrapy.Field()
    title = scrapy.Field()
    type = scrapy.Field()
    commentId = scrapy.Field()
    commentDate = scrapy.Field()
    commentContent = scrapy.Field()


class YoukuItem(scrapy.Item):
    comment = scrapy.Field()
    userId = scrapy.Field()