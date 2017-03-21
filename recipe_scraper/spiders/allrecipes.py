# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import SitemapSpider
from recipe_scraper.items import RecipeItem
from subprocess import check_output

class AllrecipesSpider(SitemapSpider):
    name = "allrecipes"
    gitBase = check_output('git rev-parse --show-toplevel', shell=True)
    gitBase = gitBase.decode('utf-8').strip()
    filenames = ['recipedetail.xml']
    sitemap_urls = []
    for file in filenames:
        sitemap_urls.append('file://' + gitBase + "/recipe_scraper/spiders/allrecipesSitemap/" + file)

    def parse(self, response):
        pass
