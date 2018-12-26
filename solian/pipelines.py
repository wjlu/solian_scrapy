# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import time
from solian.items import UserItem
from scrapy.conf import settings
from solian.psqlrequest import *
from solian import emailSender
import logging

class TimestampPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, UserItem):
            if item.get('content'):
                item['content'] = item['content'].strip().replace('\n','').replace('\r','').replace('\xa0','')
            if item.get('title'):
                item['title'] = item['title'].strip().replace('\n','').replace('\r','').replace('\xa0','')
            if item.get('timestamp'):
                item['date'] = time.strftime("%Y年%m月%d日 %H:%M:%S", time.localtime(item.get('timestamp')))
            # 增加url是否为空的判断
            print(type(item['url']))
            if item.get('url') == '' :
                print('进入')
                if item.get('source') == '共享财经':
                    item['url']= 'http://www.gongxiangcj.com/short_news'
                if item.get('source')=='金色财经':
                    item['url'] = 'https://www.jinse.com/lives'
                    print('进入金色财经')
                if item.get('source')=='火讯财经':
                    item['url'] = 'https://huoxun.com/lives.html'
                    print('进入火讯财经')
                if item.get('source')=='未来财经':
                    item['url'] = 'http://www.weilaicaijing.com/NowExpress'
                if item.get('source')=='币快财经':
                    item['url'] = 'http://www.bikuai.org/kuaibao.php'
                if item.get('source')=='耳朵财经':
                    item['url'] = 'http://www.iterduo.com/news'
                else:
                    emailSenderClient = emailSender()
                    toSendEmailLst = ['844916536@qq.com', 'lwj.198@163.com']
                    subject = '插入新网站'
                    emailSenderClient.sendEmail(toSendEmailLst, subject, body=None)
                    self.logger.ERROR('插入新网站%s') % item.get('source')
        return item


class MongoPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):
    collection_name = settings.get('CO')

    def __init__(self, mongo_uri, mongo_db):
        self.logger = logging.getLogger(__name__)
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=settings.get('MONGO_URI'),
            mongo_db=settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # self.logger.debug(item)
        myquery = {"id": item['id']}
        # 没有找到则插入表，设置字段为1，并用这个字段判断发送邮件
        # db.users.find({"id": '0b3ab35e6a6902'}).count();
        if self.db[self.collection_name].find(myquery).count() == 0:
            item['purl'] = '1'
            # begin ----发送request请求，增加psql数据-#
            data = {
                "title": item['title'],
                "lang": "zh_cn",
                "platform": 4,
                "category": 2,
                "content_mark": "",
                "content_html": item['content'],
                "original": False,
                "original_url": item['url']
            }
            response = post(data)
            # end ----发送request请求，增加psql数据-#
            # b 对插入psql打印状态码  #
            if str(response.status_code) == '201':
                self.logger.debug(response.status_code)
                self.logger.info(response.text)
            else:
                #并发送邮件通知psql插入失败  #
                emailSenderClient = emailSender()
                toSendEmailLst = ['844916536@qq.com', 'lwj.198@163.com']
                subject = 'psql插入失败通知'
                emailSenderClient.sendEmail(toSendEmailLst, subject, body=None)
                self.logger.ERROR('插入psql报错，状态码为%s') % response.status_code
                self.logger.info(response.text)
            # e 对插入psql打印状态码
            # b 对mongodb 插入数据并置位1
            self.db[self.collection_name].update(myquery, dict(item), True)
        elif self.db[self.collection_name].find(myquery).count() == 1:
            item['purl'] = '2'
            self.db[self.collection_name].update_one(myquery, {'$set':{'purl': '2'}})
        else:
            self.logger.ERROR('there ie error')

        return item

