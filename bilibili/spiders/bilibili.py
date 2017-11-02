# -*- coding: utf-8 -*-
import psycopg2
import scrapy

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
        Title = select.xpath('/html/body/div[4]/div[1]/div[2]/div[1]/div[1]/h1/text()').extract()
        Date = select.xpath('/html/body/div[4]/div[1]/div[2]/div[1]/div[3]/time/i/text()').extract()
        Plays = select.xpath('//*[@id="dianji"]/text()').extract()
        Comments = select.xpath('//*[@id="dm_count"]/text()').extract()
        Coins = select.xpath('//*[@id="v_ctimes"]/text()').extract()
        Collects = select.xpath('//*[@id="stow_count"]/text()').extract()
        Videosrc = select.xpath('/html/body/div[4]/div[2]/div[3]/div[1]/div/div[1]/div[2]/div[5]/video/@src').extract()
        Content = select.xpath('//*[@id="v_desc"]/text()').extract()
        Imgsrc = select.xpath('/html/body/img/@src').extract()
        Username = select.xpath('/html/body/div[4]/div[1]/div[2]/div[2]/div[2]/div[1]/a[1]/text()').extract()
        Userimgsrc = select.xpath('/html/body/div[4]/div[1]/div[2]/div[2]/div[1]/a[1]/img/@src').extract()
        Usercontent = select.xpath('/html/body/div[4]/div[1]/div[2]/div[2]/div[2]/div[2]/text()').extract()
        print(Videosrc)
        """print(Title)
        print(Date)
        print(Plays)
        print(Comments)
        print(Coins)
        print(Collects)
        print(Videosrc)
        print(Content)
        print(Imgsrc)
        print(Username)
        print(Userimgsrc)
        print(Usercontent)"""
        