# -*- coding: utf-8 -*-
import scrapy
from recipe_scraper.items import RecipeItem

class AllrecipesSpider(scrapy.Spider):
    name = "allrecipes"
    start_urls = ['http://allrecipes.com/recipes/1947/everyday-cooking/quick-and-easy/']

    def parse(self, response):
        pass
