# -*- coding: utf-8 -*-
from scrapy import Selector
from scrapy import Request
from scrapy import signals
from scrapy.spiders import Spider
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.xlib.pydispatch import dispatcher

from selenium import webdriver

from bilibili.items import BilibiliItem

import re
import time
import random


# Spider
class BilibiliSpider(Spider):
    name = 'bilibili'
    allowed_domains = ['bilibili.com']
    start_urls = [
        "https://www.bilibili.com/"
    ]

    def __init__(self):
        print('='*12 + ' PhantomJS ' + '='*12)
        print("> PhantomJS is starting...")
        self.driver = webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs')
        self.driver.set_page_load_timeout(30)
        super(BilibiliSpider, self).__init__()
        dispatcher.connect(self.spider_closed,signals.spider_closed)

    def spider_closed(self, spider):
        print('='*12 + ' PhantomJS ' + '='*12)
        print("> PhantomJS is closing...")
        self.driver.quit()

    def parse(self, response):
        print('='*12 + '  Spider  ' + '='*12)
        print('> Spider is parsing...')
        select = Selector(response)
        items_urls = select.xpath('//*[@id="primary_menu"]/ul/li/a/@href').extract()
        video = re.compile('//www.bilibili.com/video/(.*).html')
        for items_url in items_urls:
            if video.match(items_url):
                yield Request(
                    url='https:' + items_url,
                    callback=self.parse_items,
                )

    def parse_items(self, response):
        print('='*12 + '  Spider  ' + '='*12)
        print('[%s]> Spider is parsing items...'%(response.url.split('.')[2].split('/')[-1]))
        select = Selector(response)
        item_urls = select.xpath('//a[@target="_blank"]/@href').extract()
        av = re.compile('/video/av(.*)')
        for item_url in item_urls:
            if av.match(item_url):
                Id = av.split(item_url)[1]
                yield Request(
                    url= 'http://www.bilibili.com' + item_url,
                    meta={
                        'Id': Id,
                    },
                    callback=self.parse_details,
                )

    def parse_details(self, response):
        print('='*12 + '  Spider  ' + '='*12)
        print('[%s]> Spider is parsing Details...'%(response.url.split('/')[-2]))
        # print("> Random sleeping...")
        # time.sleep(abs(random.gauss(3, 0.5)))
        select = Selector(response)
        item = BilibiliItem()
        item['Id'] = response.meta['Id']
        item['Title'] = select.xpath('/html/body/div[4]/div[1]/div[2]/div[1]/div[1]/h1/text()').extract()[0]
        try:
            item['Date'] = select.xpath('/html/body/div[4]/div[1]/div[2]/div[1]/div[3]/time/i/text()').extract()[0]
        except IndexError:
            item['Date'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        Plays = select.xpath('//*[@id="viewbox_report"]/div[1]/div[4]/div[1]/@title').extract()[0]
        item['Plays'] = re.findall('([0-9]+)', Plays)[0]
        Comments = select.xpath('//*[@id="viewbox_report"]/div[1]/div[4]/div[2]/@title').extract()[0]
        item['Comments'] = re.findall('[0-9]+', Comments)[0]
        Coins = select.xpath('//*[@id="viewbox_report"]/div[1]/div[4]/div[4]/@title').extract()[0]
        item['Coins'] = re.findall('[0-9]+', Coins)[0]
        Collects = select.xpath('//*[@id="viewbox_report"]/div[1]/div[4]/div[5]/@title').extract()[0]
        item['Collects'] = re.findall('[0-9]+', Collects)[0]
        # item['Videosrc'] = select.xpath('//*[@id="bilibiliPlayer"]/div[1]/div[2]/div[6]/video/@src').extract()[0]
        item['Videosrc'] = 'TODO'
        item['Content'] = select.xpath('//*[@id="v_desc"]/text()').extract()[0]
        item['Imgsrc'] = select.xpath('/html/body/img/@src').extract()[0]
        item['Username'] = select.xpath('/html/body/div[4]/div[1]/div[2]/div[2]/div[2]/div[1]/a[1]/text()').extract()[0]
        item['Userimgsrc'] = select.xpath('/html/body/div[4]/div[1]/div[2]/div[2]/div[1]/a[1]/img/@src').extract()[0]
        try:
            item['Usercontent'] = select.xpath('/html/body/div[4]/div[1]/div[2]/div[2]/div[2]/div[2]/text()').extract()[0]
        except IndexError:
            item['Usercontent'] = ''
        yield item
        

# CrawlSpider
class BilibiliCrawlSpider(CrawlSpider):
    print('='*12 + '  Spider  ' + '='*12)
    print('> Spider is initing...')
    name = 'bilibilicrawl'
    allowed_domains = ['bilibili.com']
    start_urls = [
        # "https://www.bilibili.com/"
        "https://www.bilibili.com/video/game.html"
    ]
    rules = [
        Rule(LinkExtractor(allow=[r'//www.bilibili.com/video/av(.*)/']), 'parse_item')
    ]
    def __init__(self):
        print('='*12 + ' PhantomJS ' + '='*12)
        print("> PhantomJS is starting...")
        self.driver = webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs')
        self.driver.set_page_load_timeout(30)
        super(BilibiliCrawlSpider, self).__init__()
        dispatcher.connect(self.spider_closed,signals.spider_closed)

    def spider_closed(self, spider):
        print('='*12 + ' PhantomJS ' + '='*12)
        print("> PhantomJS is closing...")
        self.driver.quit()

    def parse_item(self, response):
        print('='*12 + '  Spider  ' + '='*12)
        print('> Spider is parsing...')
        print("> Random sleeping...")
        time.sleep(abs(random.gauss(3, 0.5)))
        item = BilibiliItem()
        item['Id'] = response.url
        select = Selector(response)
        item['Videosrc'] = select.xpath('//*[@id="bilibiliPlayer"]/div[1]/div[2]/div[6]/video/@src').extract()[0]
        yield item
