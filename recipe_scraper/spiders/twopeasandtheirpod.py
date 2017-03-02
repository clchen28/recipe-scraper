# -*- coding: utf-8 -*-
import scrapy


class TwopeasandtheirpodSpider(scrapy.Spider):
    name = "twopeasandtheirpod"
    start_urls = ['http://www.twopeasandtheirpod.com/category/recipes/main-dishes/']

    # prepTime comes out in the following format: PT45M, or PT8H10M
    # Need to parse this to "45 minutes" or "8 hours 10 minutes"
    def parse(self, response):
        recipe = response.css("div.recipe")
        if recipe:
            yield {
            'title': recipe.css("h2").css("span::text").extract_first(),
            'URL': response.url,
            'imgURL': recipe.css("div.recipebody").css("img").xpath("@src").extract_first(),
            'description': recipe.css("div.summary").css("p::text").extract_first(),
            'cuisine': None,
            'prepTime': recipe.css("div.time").css("meta[itemprop=totalTime]").xpath("@content").extract_first()
            }
        else:
            # archives div contains all blog posts, item div represents a
            # specific post

            # Including this section under else statement, since recipe pages
            # also have an archives div
            links = response.css("div.archives").css("div.item").css("a").xpath("@href").extract()
            if links:
                for link in links:
                    yield scrapy.Request(link, callback=self.parse)
