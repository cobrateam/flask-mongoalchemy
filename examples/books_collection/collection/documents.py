from collection import db
from flaskext.mongoalchemy import BaseQuery
import re

class BookQuery(BaseQuery):

    def starting_with(self, letter):
        regex = r'^' + letter
        return self.filter({'title' : re.compile(regex, re.IGNORECASE)})

class Book(db.Document):
    query_class = BookQuery

    title = db.StringField()
    year = db.IntField()
