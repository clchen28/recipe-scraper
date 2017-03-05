# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class RecipeItem(scrapy.Item):
    title = scrapy.Field()
    URL = scrapy.Field()
    imgURL = scrapy.Field()
    description = scrapy.Field()
    cuisine = scrapy.Field()
    prepTime = scrapy.Field()
