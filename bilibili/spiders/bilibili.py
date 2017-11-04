# -*- coding: utf-8 -*-
from scrapy import Selector
from scrapy import Request
from scrapy.spiders import Spider
import re

from bilibili.items import BilibiliItem

class BilibiliSpider(Spider):
    name = 'bilibili'
    allowed_domains = ['bilibili.com']
    start_urls = [
        "https://www.bilibili.com/"
    ]

    def parse(self, response):
        select = Selector(response)
        items_urls = select.xpath('//*[@id="primary_menu"]/ul/li/a/@href').extract()
        for items_url in items_urls:
            yield Request(
                url='https:' + items_url,
                callback=self.parse_item,
            )

    def parse_item(self, response):
        select = Selector(response)
        item_urls = select.xpath('//a[@target="_blank"]/@href').extract()
        av = re.compile('//www.bilibili.com/video/av(.*)/')
        for item_url in item_urls:
            if av.match(item_url):
                Id = av.split(item_url)[1]
                yield Request(
                    url= 'https:' + item_url,
                    meta={
                        'Id': Id,
                    },
                    callback=self.parse_details,
                )

    def parse_details(self, response):
        select = Selector(response)
        item = BilibiliItem()
        item['Id'] = response.meta['Id']
        item['Title'] = select.xpath('/html/body/div[4]/div[1]/div[2]/div[1]/div[1]/h1/text()').extract()[0]
        try:
            item['Date'] = select.xpath('/html/body/div[4]/div[1]/div[2]/div[1]/div[3]/time/i/text()').extract()[0]
        except IndexError:
            item['Date'] = ''
        Plays = select.xpath('//*[@id="viewbox_report"]/div[1]/div[4]/div[1]/@title').extract()[0]
        item['Plays'] = re.findall('([0-9]+)', Plays)[0]
        Comments = select.xpath('//*[@id="viewbox_report"]/div[1]/div[4]/div[2]/@title').extract()[0]
        item['Comments'] = re.findall('[0-9]+', Comments)[0]
        Coins = select.xpath('//*[@id="viewbox_report"]/div[1]/div[4]/div[4]/@title').extract()[0]
        item['Coins'] = re.findall('[0-9]+', Coins)[0]
        Collects = select.xpath('//*[@id="viewbox_report"]/div[1]/div[4]/div[5]/@title').extract()[0]
        item['Collects'] = re.findall('[0-9]+', Collects)[0]
        # item['Videosrc'] = select.xpath('/html/body/div[4]/div[2]/div[3]/div[1]/div/div[1]/div[2]/div[5]/video/@src').extract()[0]
        item['Videosrc'] = 'TODO'
        item['Content'] = select.xpath('//*[@id="v_desc"]/text()').extract()[0]
        item['Imgsrc'] = 'https:' + select.xpath('/html/body/img/@src').extract()[0]
        item['Username'] = select.xpath('/html/body/div[4]/div[1]/div[2]/div[2]/div[2]/div[1]/a[1]/text()').extract()[0]
        item['Userimgsrc'] = 'https:' + select.xpath('/html/body/div[4]/div[1]/div[2]/div[2]/div[1]/a[1]/img/@src').extract()[0]
        try:
            item['Usercontent'] = select.xpath('/html/body/div[4]/div[1]/div[2]/div[2]/div[2]/div[2]/text()').extract()[0]
        except IndexError:
            item['Usercontent'] = ''
        yield item
        