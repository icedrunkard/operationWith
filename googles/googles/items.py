# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GooglesItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    url = scrapy.Field()
    topcard = scrapy.Field()
    summary = scrapy.Field()
    experience = scrapy.Field()
    education = scrapy.Field()
    publications = scrapy.Field()
    projects = scrapy.Field()
    awards = scrapy.Field()
    skills = scrapy.Field()
    organizations = scrapy.Field()
    languages = scrapy.Field()
    certifications = scrapy.Field()
    scores = scrapy.Field()
    
