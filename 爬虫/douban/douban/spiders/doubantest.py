import json
import re
import scrapy
import logging

from douban.items import DoubanItem

class DoubantestSpider(scrapy.Spider):
    name = 'doubantest'
    allowed_domains = ['douban.com']

    book_ids = ['25897657']

    def start_requests(self):
        for id in self.book_ids:
            root_ = 'https://book.douban.com/subject/%s/reviews?start=' % id
            yield scrapy.Request(root_ + '0', meta={'root': root_}, callback=self.get_pages)

    def get_pages(self, response):
        root_ = response.meta['root']
        self.parse(response)
        a_text = response.css("#content > div > div.article > div.paginator > a::text")
        if a_text:
            pages = response.css("#content > div > div.article > div.paginator > a::text").extract()[-1]
            pages = int(pages)
        else:
            pages = 100
        logging.info("page = " + str(pages))
        for i in range(1, pages + 1):
            yield scrapy.Request(root_ + str(i * 20), meta={'objectId': id}, callback=self.parse)

    def parse(self, response):
        # 每页 20个评论数据
        reviewer_author = response.css("header > a.name::text").extract()
        title = response.css(".main-bd > h2 > a::text").extract()
        data_cid = response.css("div::attr(data-cid)").extract()

        for idx in range(len(reviewer_author)):
            item = DoubanItem()
            item['parent'] = -1
            item['reviewer_author'] = reviewer_author[idx]
            item['title'] = title[idx]
            item['data_cid'] = data_cid[idx]

            rev_json = 'https://book.douban.com/j/review/%s/full' % data_cid[idx]

            yield scrapy.Request(rev_json, meta={'item': item}, callback=self.get_json_reviewer)

            sub_comment_url = 'https://book.douban.com/review/%s/' % data_cid[idx]

            yield scrapy.Request(sub_comment_url, meta={'sub_comment_url': sub_comment_url, 'data_cid': data_cid[idx]},
                                 callback=self.parse_sub_review)

    def get_json_reviewer(self, response):
        item = response.meta['item']
        json_data = json.loads(response.text)
        item['reviewer_content'] = json_data.get('html', '')
        return item

    def parse_sub_review(self, response):

        parent_id = response.meta['data_cid']
        script = response.text
        d = re.search(re.compile("'comments': (.*)"), script)
        if d:
            if not d.group():
                logging.log(response.meta['sub_comment_url'])
            else:
                json_text = d.group().strip("'comments':").strip(",")
                info = json.loads(json_text)

                for review in info:
                    item = DoubanItem()
                    item['parent'] = parent_id
                    item['reviewer_author'] = review['author']['name']
                    item['title'] = ''
                    item['data_cid'] = review['id']
                    item['reviewer_content'] = review['text']
                    yield item