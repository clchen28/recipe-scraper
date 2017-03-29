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
        # Convert prep time from "PT##H##M" into minutes
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


# Converts "PT#H##M" or similar into total time in minutes, as a string
def parse_prep_time(pt):
    # Strip off "PT" 
    pt = pt[pt.index('PT') + 2:]

    hours = minutes = 0
    
    # Times without minutes 
    if "M" not in pt:
        # Strip everything after and including the 'H'
        pt = pt[:pt.index('H')]
        hours = int(pt)
    # Times with minutes
    else:
        # strip everything after and including the 'M'
        pt = pt[:pt.index('M')]

        if "H" not in pt:
            minutes = int(pt)
        else:
            (hours, minutes) = [int(s) for s in pt.split('H', 1)]

    return str(hours*60 + minutes)
