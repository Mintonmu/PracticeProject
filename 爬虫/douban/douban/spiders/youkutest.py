# -*- coding: utf-8 -*-
import json

import emoji
import scrapy
from PyQt5.QtWidgets import QTextEdit
from scrapy import Request

from douban.items import YoukuItem


class YoukutestSpider(scrapy.Spider):
    name = 'youkutest'
    allowed_domains = ['youku.com']

    start_objectId = [1201893336]

    def start_requests(self):
        for id in self.start_objectId:
            url = self.get_real_url(1, id)
            yield Request(url, meta={'objectId': id}, method="GET")

    def parse(self, response):
        objectId = response.meta['objectId']
        text = response.text[16:-1]
        response_dict = json.loads(text)
        # 获取总页数
        total_page = response_dict['data']['totalPage']

        # 遍历第一页
        for i in response_dict['data']['comment']:
            comment = emoji.demojize(str(i['content']))
            c = YoukuItem()
            c['comment'] = str(comment)
            yield c

        # 循环其他页
        for j in range(2, total_page + 1):
            yield Request(self.get_real_url(j, objectId), method='GET', callback=self.get_comment)

    def get_comment(self, response):
        text = response.text[16:-1]
        # 用json.loads(str) 转换成字典
        response_dict = json.loads(text)
        # 遍历该页的评论
        open('a.txt', 'w').write(str(response_dict))

        for i in response_dict['data']['comment']:

            userId = str(i['userId'])
            comment = emoji.demojize(str(i['content']))
            c = YoukuItem()
            c['userId'] = userId
            c['comment'] = str(comment)
            yield c

    def get_real_url(self, page, objectId):
        payload = {
            'jsoncallback': 'n_commentList',
            'app': '100-DDwODVkv',
            'objectId': str(objectId),
            'objectType': '1',
            'listType': '0',
            'currentPage': str(page),
            'pageSize': '30',
            'sign': 'edcc3e3b6c345339a426f93dbd9f05ca',
            'time': '1553254978'
        }

        url = 'https://p.comments.youku.com/ycp/comment/pc/commentList?'
        for key, value in payload.items():
            url += key + "=" + value + "&"
        return url
