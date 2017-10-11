# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class MaimaiNumItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id=Field()
    all=Field()
    name=Field()
    py=Field()
    position=Field()
    work_exp=Field()
    education=Field()
    encode_mmid=Field()


