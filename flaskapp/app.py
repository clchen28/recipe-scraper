# Adapted from https://impythonist.wordpress.com/2015/07/12/build-an-api-under-30-lines-of-code-with-python-and-flask/

from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import *
from sqlalchemy.orm import create_session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('sqlite:///recipes.db')
metadata = MetaData(bind=engine)

class Recipes(Base):
    __table__ = Table('Recipes', metadata, autoload=True)

session = create_session(bind=engine)

# http://docs.sqlalchemy.org/en/latest/orm/session_basics.html#querying
# allRecipes = session.query(Recipes).all()

app = Flask(__name__)
api = Api(app)

class searchRecipeTitle(Resource):
    def get(self, searchTerm):
        searchStr = '%' + searchTerm + '%'
        # results will be an empty list if the search term is not found
        results = \
        session.query(Recipes).filter(Recipes.title.like(searchStr)).all()

        # response is a dict which represents the API's response at this
        # endpoint
        response = {}
        response["count"] = len(results)
        response["recipes"] = []

        for row in results:
            rowData = {}
            rowData["id"] = row.id
            rowData["title"] = row.title
            rowData["URL"] = row.URL
            rowData["imgURL"] = row.imgURL
            rowData["cuisine"] = row.cuisine
            rowData["prepTime"] = row.prepTime
            response["recipes"].append(rowData)

        # return JSON data (dict automatically converted to JSON)
        return response

api.add_resource(searchRecipeTitle, '/search/title/<searchTerm>')

if __name__ == '__main__':
     app.run()
