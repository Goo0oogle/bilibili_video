# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import psycopg2


class BilibiliPipeline(object):
    def process_item(self, item, spider):
        return item


class PostgrePipeline(object):
    def __init__(self, *args):
        super(PostgrePipeline, self).__init__(*args)
        print('Postgresql is starting...')

    def open_spider(self, spider):
        print('Ready!')
    
    def close_spider(self, spider):
        print('Done!')

    def process_item(self, item, spider):
        print('Database is connecting...')
        self.db = psycopg2.connect(
            database='videoinfodb',
            user='ubuntu',
            password='wyq2644756656',
            host='111.230.15.157',
            port='5432'
        )
        print('Cursor is creating...')
        self.cursor = self.db.cursor()
        print('processing items...') 
        try:
            self.cursor.execute(
                "insert into videoinfo(id,title,date,plays,comments,coins,collects,videosrc,content,imgsrc,username,userimgsrc,usercontent) values (%s, '%s', '%s', %s, %s, %s, %s, '%s', '%s', '%s', '%s', '%s', '%s')"
                %(
                    item['Id'],
                    item['Title'],
                    item['Date'],
                    item['Plays'],
                    item['Comments'],
                    item['Coins'],
                    item['Collects'],
                    item['Videosrc'],
                    item['Content'],
                    item['Imgsrc'],
                    item['Username'],
                    item['Userimgsrc'],
                    item['Usercontent']
                )
            )
        except psycopg2.ProgrammingError as err:
            print('raise an error:' + err)
        else:    
            self.db.commit()
        print('items has been processed...')
        self.db.commit()
        print('Changes has been committed...')
        print('Database is closing...')
        self.db.close()
