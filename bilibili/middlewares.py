# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
# from selenium.common.exceptions import TimeoutException
from urllib.error import URLError
from scrapy.http import HtmlResponse
from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware
from bilibili.settings import USER_AGENTS
from bilibili.settings import HTTP_PROXIES

import sys
import time
import random


class RandomUserAgent(UserAgentMiddleware):
    def __init__(self, user_agent=''):
        super(RandomUserAgent, self).__init__()
        self.user_agent = user_agent

    def process_request(self, request, spider):
        print('='*12 + ' User-Agent ' + '='*12)
        print('> Randoming User-Agent...')
        user_agent = random.choice(USER_AGENTS)
        print('> Select User-Agent: %s'%user_agent)
        request.headers.setdefault('User-Agent', user_agent)


class RandomHttpProxy(object):
    def process_request(self, request, spider):
        print('='*12 + ' Http-Proxy ' + '='*12)
        print('> Randoming Http-Proxy...')
        http_proxy = random.choice(HTTP_PROXIES)
        print('> Select Http-Proxy: %s'%http_proxy)
        request.meta['proxy'] = http_proxy
        
        
class PhantomJSMiddleware(object):
    @classmethod
    def process_request(self, request, spider):
        print('='*12 + ' PhantomJS ' + '='*12)
        print("> 访问 " + request.url)
        try:
            spider.driver.get(request.url)
        except URLError:
            # print('='*12 + ' PhantomJS ' + '='*12)
            print("> 访问 " + request.url + " 被拒绝")
            spider.driver.execute_script('window.stop()')
            print("> 访问暂停")
            time.sleep(30)

        # print('='*12 + ' PhantomJS ' + '='*12)
        print("> Random sleeping...")
        time.sleep(abs(random.gauss(1, 0.3)))

        print("> Start loading javaScript...")
        js = "window.scrollTo(0, document.body.scrollHeight/20*{});"
        for i in range(20):
            # print('='*12 + ' PhantomJS ' + '='*12)
            sys.stdout.write("[%3d"%((i+1)*5) + "%]> JavaScript is loading...\r")
            sys.stdout.flush()
            time.sleep(abs(random.gauss(0.5, 0.1)))
            spider.driver.execute_script(js.format(i+1))

        sys.stdout.write('\n')
        # print('='*12 + ' PhantomJS ' + '='*12)
        print("> JavaScript is loaded...")
        time.sleep(abs(random.gauss(1, 0.3)))
        
        print("> Getting page Content...")
        content = spider.driver.page_source.encode('utf-8')
        
        return HtmlResponse(request.url, encoding='utf-8', body=content, request=request)


class BilibiliSpiderMiddleware(object):
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

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
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
