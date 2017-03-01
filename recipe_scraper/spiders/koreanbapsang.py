# -*- coding: utf-8 -*-
import scrapy

class KoreanbapsangSpider(scrapy.Spider):
    name = "koreanbapsang"
    start_urls = ['http://www.koreanbapsang.com/2017/']

    def parse(self, response):
        # Each recipe on this level is contained in a div with class "main dish"
        # reponse.css("div.main-dish") would return all of the divs with class main-dish
        # [0] selects a specific one, i.e., the first one

        # recipe1 = response.css("div.post")[0]
        # recipe1title = response.css("div.post")[0].css("a::text").extract()

        # Ideally, crawl until you hit a site with the yumprint tags
        recipe = response.css("div.blog-yumprint-recipe-title::text")
        if recipe:
            yield {
            'title': recipe.extract_first(),
            'URL': response.url,
            'imgURL': response.css("img.blog-yumprint-photo-top-large").xpath('@src').extract_first(),
            'description': response.css("div.blog-yumprint-recipe-summary::text").extract_first(),
            'cuisine': 'Korean',
            'prepTime': None
            }

        links = response.css("a.entry-image-link").xpath("@href").extract()
        if links:
            for link in links:
                yield scrapy.Request(link, callback=self.parse)