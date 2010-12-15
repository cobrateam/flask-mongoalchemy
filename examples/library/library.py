# -*- coding: utf-8 -*-
"""
    Flask-MongoAlchemy library example
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    A simple example showing the use of Flask-MongoAlchemy.

    If you want to test it:

        - install MongoDB, Flask, MongoAlchemy, pymongo and Flask-MongoAlchemy;
        - run on terminal:
            python library.py

    :copyright: (c) 2010 by Francisco Souza.
    :license: BSD, see LICENSE for more details.
"""

from flask import Flask, request
from flaskext.mongoalchemy import MongoAlchemy
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['MONGOALCHEMY_DATABASE'] = 'library'
db = MongoAlchemy(app)

class Author(db.Document):
    name = db.StringField()

class Book(db.Document):
    title = db.StringField()
    author = db.DocumentField(Author)
    year = db.IntField()

@app.route('/author/new')
def new_author():
    """Creates a new author by a giving name (via GET parameter)

    e.g.: GET /author/new?name=Francisco creates a author named Francisco
    """
    author = Author(name=request.args.get('name', ''))
    author.save()
    return 'Saved :)'

@app.route('/authors/')
def list_authors():
    """List all authors.

    e.g.: GET /authors"""
    authors = Author.query.all()
    content = '<p>Authors:</p>'
    for author in authors:
        content += '<p>%s</p>' % author.name
    return content

if __name__ == '__main__':
    app.run()
