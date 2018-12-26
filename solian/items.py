# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class UserItem(Item):
    # define the fields for your item here like:
    category = Field()
    content = Field()
    date = Field()
    id = Field()
    purl = Field()
    source = Field()
    timestamp = Field()
    title = Field()
    url = Field()
