# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    salary_min = scrapy.Field()
    salary_max = scrapy.Field()

    salary_type = scrapy.Field()
    experience_min = scrapy.Field()
    experience_max = scrapy.Field()

    job_title = scrapy.Field()
    city_name = scrapy.Field()
    addr = scrapy.Field()
    #email = scrapy.Field()
    job_nature = scrapy.Field()
    jd = scrapy.Field()
    degree = scrapy.Field()
    #start_at = scrapy.Field()
    #end_at = scrapy.Field()
    source = scrapy.Field()
    frequency = scrapy.Field()
    #duration = scrapy.Field()
    company_cn = scrapy.Field()
    #company_nature = scrapy.Field()
    company_scale = scrapy.Field()
    industry_name = scrapy.Field()
    company_intro = scrapy.Field()
    logo_url = scrapy.Field()
