# -*- coding: utf-8 -*-
import scrapy
from recipe_scraper.items import RecipeItem
import re

class Simplyrecipesspider(scrapy.Spider):
    name = "simplyrecipes"
    start_urls = ['http://www.simplyrecipes.com/recipes/course/dinner/']

    def parse(self, response):
        recipeDescription = response.css("article.recipe").css('meta[itemprop="description"]').xpath("@content")

        recipe = response.css("div.recipe-callout")
        if recipe:
            tags = response.css('span[itemprop="recipeCategory"]').css("a").xpath("@href").extract()

            # Checks to see if the recipe has a cuisine tag
            if tags:
                cuisineTag = [tag for tag in tags if re.search("cuisine",tag)]

            # If the recipe has a cuisine tag, include it in the result
            recipeCuisine = ""
            if cuisineTag:
                recipeCuisine = response.css('span[itemprop="recipeCategory"]').css('a[href="' + cuisineTag[0] + '"]').css("a::text").extract_first()

            yield RecipeItem(title = recipe.css("h2::text").extract_first(),
            URL = response.url,
            imgURL = response.css("div.entry-content").css("div.featured-image").css("img.photo").xpath("@src").extract_first(),
            description = response.css("article.recipe").css('meta[itemprop="description"]').xpath("@content").extract_first(),
            cuisine = recipeCuisine,
            prepTime = response.css("span.cooktime").xpath("@content").extract_first()
            )
        else:
            links = response.css("li.recipe").css("a").xpath("@href").extract()
            if links:
                for link in links:
                    yield scrapy.Request(link, callback=self.parse)

            # If the current page is a navigation page, goes through next page
            # link until there are no more recipes to scrape
            nextLink = response.css("a.page-numbers.next").xpath("@href").extract_first()
            if nextLink:
                yield scrapy.Request(nextLink, callback=self.parse)
