# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScholarItem(scrapy.Item):
    # define the fields for your item here like:
    #playload=scrapy.Field()
    #key=scrapy.Field()
    school_url = scrapy.Field()
    school_name = scrapy.Field()
    #school_baseid=scrapy.Field()
    #school_pcode=scrapy.Field()
    #school_title=scrapy.Field()
    #school_location=scrapy.Field()
    #paper_pages= scrapy.Field()

    
class Scholar2Item(scrapy.Item):
    # define the fields for your item here like:
    school_name = scrapy.Field()
    school_baseid=scrapy.Field()
    school_pcode=scrapy.Field()
    school_title=scrapy.Field()
    school_location=scrapy.Field()
    paper_pages= scrapy.Field()

    
    paper_name= scrapy.Field()
    paper_path= scrapy.Field()
    
    author= scrapy.Field()
    tutor= scrapy.Field()
    
    degree_year= scrapy.Field()
    degree= scrapy.Field()
    keywords= scrapy.Field()
    udc= scrapy.Field()
