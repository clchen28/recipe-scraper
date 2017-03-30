# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3
import re
import isodate
from recipe_scraper.items import RecipeItem

class RecipeScraperPipeline(object):
    def open_spider(self, spider):
        self.recipeDB = sqlite3.connect("./db/recipes.db")
        self.cursor = self.recipeDB.cursor()

    def close_spider(self, spider):
        self.recipeDB.close()

    def process_item(self, item, spider):
        if item['prepTime']:
            item['prepTime'] = parse_prep_time(item['prepTime'])
        curRow = self.cursor.execute("SELECT * FROM RECIPES WHERE URL=?",
            (item['URL'],))
        if (curRow.fetchone() == None):
            self.storeItemInDB(item)
        return item

    def storeItemInDB(self, item):
        self.cursor.execute(
        "INSERT INTO RECIPES \
        (title, URL, imgURL, description, cuisine, prepTime) \
        VALUES \
        (?, ?, ?, ?, ?, ?)",
        (item['title'], item['URL'], item['imgURL'],
        item['description'], item['cuisine'], item['prepTime'])
        )

        self.recipeDB.commit() # Save the changes

def parse_prep_time(pt):
    mMatch = re.search("[0-9]M", pt)

    # Strips any extraneous text after M
    if mMatch:
        pt = pt[0:mMatch.end()]

        # parse_duration method parses ISO 8601 string to a timedelta, and
        # total_seconds converts to a float

        pt = int(isodate.parse_duration(pt).total_seconds() / 60) # minutes
        return pt
