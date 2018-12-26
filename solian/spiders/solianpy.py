# -*- coding: utf-8 -*-
from scrapy import *
import json
from solian.items import UserItem
from solian.emailSender import emailSender  # 导入发信模块
import datetime

class SolianpySpider(Spider):
    name = 'solianpy'
    allowed_domains = ['solian.net']
    start_urls = 'http://solian.net:9233/article/searchflash?'
    max_page = 10

    def start_requests(self):
        for page in range(1,self.max_page + 1):
            url = '{url}page={page}&offset=10'.format(url=self.start_urls, page=page)
            yield Request(url, callback=self.parse_detail)


    def parse_detail(self, response):
        url = response.url
        result = json.loads(response.text)
        # print(result.get('data'))

        item = UserItem()
        for i in result.get('data'):
            for field in item.fields:
                if field in i.keys():
                    item[field] = i.get(field)
            yield item


    def closed(self,reason):
        emailSenderClient = emailSender()
        toSendEmailLst = ['844916536@qq.com', 'lwj.198@163.com']
        finishTime = datetime.datetime.now()
        subject='solian小时消息'
        emailSenderClient.sendEmail(toSendEmailLst, subject)