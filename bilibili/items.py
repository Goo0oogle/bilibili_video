# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BilibiliItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Id = scrapy.Field()
    Title = scrapy.Field()
    Date = scrapy.Field()
    Plays = scrapy.Field()
    Comments = scrapy.Field()
    Coins = scrapy.Field()
    Collects = scrapy.Field()
    Videosrc = scrapy.Field()
    Content = scrapy.Field()
    Imgsrc = scrapy.Field()
    Username = scrapy.Field()
    Userimgsrc = scrapy.Field()
    Usercontent = scrapy.Field()
