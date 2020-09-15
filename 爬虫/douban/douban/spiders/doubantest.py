import json
import re
import scrapy
import logging

from douban.items import DoubanItem

class DoubantestSpider(scrapy.Spider):
    name = 'doubantest'
    allowed_domains = ['douban.com']

    book_ids = ['1205054']

    def start_requests(self):
        for id in self.book_ids:
            root_ = 'https://book.douban.com/subject/%s/reviews?start=' % id
            yield scrapy.Request(root_ + '0', meta={'root': root_}, callback=self.get_pages, dont_filter=True)

    def get_pages(self, response):
        root_ = response.meta['root']
        a_text = response.css("#content > div > div.article > div.paginator > a::text")
        if a_text:
            pages = response.css("#content > div > div.article > div.paginator > a::text").extract()[-1]
            pages = int(pages)
        else:
            pages = 100

        logging.info("page = " + str(pages))
        for i in range(0, pages):
            yield scrapy.Request(root_ + str(i * 20), meta={'objectId': id}, callback=self.parse)

    def parse(self, response):
        # 每页 20个评论数据
        # 一级评论
        titles = response.css(".main-bd > h2 > a::text").extract()
        commentIds = response.css("header > a.name::text").extract()
        data_cid = response.css("div::attr(data-cid)").extract()
        dates = response.css(".main-meta::attr(content)").extract()
        for idx in range(len(commentIds)):
            item = DoubanItem()
            item['parent'] = -1
            item['commentId'] = commentIds[idx]
            item['commentDate'] = dates[idx]
            item['data_cid'] = data_cid[idx]
            item['title'] = '悲惨世界'
            item['type'] = '图书'
            item['level'] = 1

            rev_json = 'https://book.douban.com/j/review/%s/full' % data_cid[idx]
            yield scrapy.Request(rev_json, meta={'item': item, 'title':titles[idx]},
                                 callback=self.get_json_commentFull)

            sub_comment_url = 'https://book.douban.com/review/%s/' % data_cid[idx]
            yield scrapy.Request(sub_comment_url, meta={'sub_comment_url': sub_comment_url,
                                                        'data_cid': data_cid[idx]},
                                 callback=self.parse_sub_review)

    def get_json_commentFull(self, response):
        item = response.meta['item']
        title = response.meta['title']
        json_data = json.loads(response.text)
        item['commentContent'] = title + '\n' + json_data.get('html', '')
        return item

    def parse_sub_review(self, response):

        parent_id = response.meta['data_cid']
        script = response.text
        d = re.search(re.compile("'comments': (.*)"), script)
        if d:
            if not d.group():
                logging.info(response.meta['sub_comment_url'])
            else:
                json_text = d.group().strip("'comments':").strip(",")
                info = json.loads(json_text)

                for review in info:
                    item = DoubanItem()
                    item['parent'] = parent_id
                    item['commentDate'] = review['create_time']
                    item['commentId'] = review['author']['name']
                    item['commentContent'] = review['text']
                    item['data_cid'] = review['id']
                    item['title'] = '悲惨世界'
                    item['type'] = '图书'
                    item['level'] = 2
                    yield item

                    sub_sub_url = f"https://book.douban.com/j/review/comment/{review['id']}/replies?start=0&count=500"
                    yield scrapy.Request(sub_sub_url, meta={'parent_id': review['id']}, callback=self.parse_sub_sub_review)


    def parse_sub_sub_review(self, response):
        parent_id = response.meta['parent_id']
        l2_comment = json.loads(response.text)
        for reply in l2_comment['replies']:
            item = DoubanItem()
            item['level'] = 3
            item['parent'] = parent_id
            item['commentContent'] = reply['text']
            item['commentId'] = reply['author']['name']
            item['commentDate'] = reply['create_time']
            item['data_cid'] = reply['id']
            item['title'] = '悲惨世界'
            item['type'] = '图书'
            yield item