# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3
from recipe_scraper.items import RecipeItem

class RecipeScraperPipeline(object):
    def open_spider(self, spider):
        self.recipeDB = sqlite3.connect("./db/recipes.db")
        self.cursor = self.recipeDB.cursor()

    def close_spider(self, spider):
        self.recipeDB.close()

    def process_item(self, item, spider):
        curRow = self.cursor.execute("SELECT * FROM RECIPES WHERE URL=?",
            (item['URL'],))
        if (curRow == None):
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
