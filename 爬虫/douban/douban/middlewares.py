# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import datetime
import json
import threading
from time import sleep

import requests
import scrapy
from scrapy import signals
import logging

import random
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

from requests.exceptions import ConnectionError

from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message
from twisted.internet.defer import DeferredLock


class DoubanSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class DoubanDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class UserAgent(UserAgentMiddleware):

    def __init__(self, user_agent=''):
        super().__init__(user_agent)

    def process_request(self, request, spider):
        ua = random.choice(self.user_agent_list)
        if ua:
            # 显示当前使用的useragent
            # print "********Current UserAgent:%s************" %ua
            # 记录
            logging.debug('Current UserAgent: ' + ua)
            request.headers.setdefault('User-Agent', ua)

    # the default user_agent_list composes chrome,I E,firefox,Mozilla,opera,netscape
    # for more user agent strings,you can find it in http://www.useragentstring.com/pages/useragentstring.php
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
        "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "
        "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "
        "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "
        "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "
        "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "
        "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "
        "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]


class ProxyIPDownloadMiddleware(object):
    def __init__(self, settings):
        self.seconds = settings.getint('expire_datetime')
        # self.expire_datetime = datetime.datetime.now() + datetime.timedelta(seconds=self.seconds)
        self.proxy = ''
        self.proxy_url = settings.get('PROXY_URL')

    def process_request(self, spider, request):
        # self._check_expire()
        request.meta['proxy'] = 'http://' + self.proxy

    def get_random_proxy(self):
        try:
            response = requests.get(self.proxy_url)
            if response.status_code == 200:
                random_proxy = response.text
                return random_proxy
        except ConnectionError:
            return False

    def _get_proxyip(self):
        logging.info("获取代理")
        self.proxy = self.get_random_proxy()
        print("-" * 20, self.proxy, '-' * 20)
        # if self.proxy:
        #    self.expire_datetime = datetime.datetime.now() + datetime.timedelta(seconds=self.seconds)

    def _check_expire(self):
        pass
        # if datetime.datetime.now() >= self.expire_datetime:
        #    self._get_proxyip()

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(settings)


class My_RetryMiddleware(RetryMiddleware):
    def __init__(self, settings):
        super(My_RetryMiddleware, self).__init__(settings)
        self.lock = DeferredLock()
        self.seconds = settings.getint('expire_datetime')
        self.proxy_url = settings.get('PROXY_URL')
        self.expire_datetime = datetime.datetime.now() + datetime.timedelta(seconds=self.seconds)
        self.proxy = None

    def process_response(self, request, response, spider):

        if request.meta.get('dont_retry', False):
            return response

        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            self._check_expire()
            request.meta['proxy'] = 'http://' + self.proxy

            return self._retry(request, reason, spider) or response
        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) and not request.meta.get('dont_retry', False):
            try:
                self._check_expire()
                if self.proxy:
                    # request.meta['proxy'] = 'http://' + self.proxy
                    request.meta['proxy'] = 'http://127.0.0.1:7890'
            except requests.exceptions.RequestException:
                spider.logger.error('获取代理ip失败！')

            return self._retry(request, exception, spider)

    def get_random_proxy(self):
        try:
            response = requests.get(self.proxy_url)
            if response.status_code == 200:
                random_proxy = response.text
                return random_proxy
            return self.proxy
        except ConnectionError:
            return self.proxy

    # def get_random_proxy(self):
    #     try:
    #         response = requests.get("http://daili.spbeen.com/get_api_json/?token=CTKMKA7YYNGz4uM3xyJySMsy&num=1")
    #         response.encoding='utf8'
    #         if response.status_code == 200:
    #             json_data = json.loads(response.text)
    #             if json_data['success']:
    #                 return json_data['data'][0]
    #
    #         return self.proxy
    #     except ConnectionError:
    #         return self.proxy

    def _get_proxyip(self):
        self.lock.acquire()
        sleep(2)
        logging.info("获取代理")
        self.proxy = self.get_random_proxy()
        print("-" * 20, self.proxy, '-' * 20)
        if self.proxy:
            self.expire_datetime = datetime.datetime.now() + datetime.timedelta(seconds=self.seconds)
        self.lock.release()

    def _check_expire(self):
        if datetime.datetime.now() >= self.expire_datetime:
            self._get_proxyip()

