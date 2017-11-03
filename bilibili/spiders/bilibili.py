# -*- coding: utf-8 -*-
import psycopg2
import scrapy

from bilibili.items import BilibiliItem

# database
db = psycopg2.connect(
    database='videoinfodb',
    user='ubuntu',
    password='wyq2644756656',
    host='111.230.15.157',
    port='5432'
)

class BilibiliSpider(scrapy.Spider):
    name = 'bilibili'
    allowed_domains = ['bilibili.com']
    start_urls = [
        # "https://www.bilibili.com/"
        "https://www.bilibili.com/video/av15924319/"
    ]

    def parse(self, response):
        select = scrapy.Selector(response)
        item = BilibiliItem()
        item['Title'] = select.xpath('/html/body/div[4]/div[1]/div[2]/div[1]/div[1]/h1/text()').extract()[0]
        item['Date'] = select.xpath('/html/body/div[4]/div[1]/div[2]/div[1]/div[3]/time/i/text()').extract()[0]
        item['Plays'] = select.xpath('//*[@id="dianji"]/text()').extract()[0]
        item['Comments'] = select.xpath('//*[@id="dm_count"]/text()').extract()[0]
        item['Coins'] = select.xpath('//*[@id="v_ctimes"]/text()').extract()[0]
        item['Collects'] = select.xpath('//*[@id="stow_count"]/text()').extract()[0]
        # item['Videosrc'] = select.xpath('/html/body/div[4]/div[2]/div[3]/div[1]/div/div[1]/div[2]/div[5]/video/@src').extract()[0]
        item['Content'] = select.xpath('//*[@id="v_desc"]/text()').extract()[0]
        item['Imgsrc'] = 'https:' + select.xpath('/html/body/img/@src').extract()[0]
        item['Username'] = select.xpath('/html/body/div[4]/div[1]/div[2]/div[2]/div[2]/div[1]/a[1]/text()').extract()[0]
        item['Userimgsrc'] = 'https:' + select.xpath('/html/body/div[4]/div[1]/div[2]/div[2]/div[1]/a[1]/img/@src').extract()[0]
        item['Usercontent'] = select.xpath('/html/body/div[4]/div[1]/div[2]/div[2]/div[2]/div[2]/text()').extract()[0]
        return item
        