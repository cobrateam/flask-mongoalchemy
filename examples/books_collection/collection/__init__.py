from flask import Flask
from flaskext.mongoalchemy import MongoAlchemy

app = Flask(__name__)
app.config['MONGOALCHEMY_DATABASE'] = 'books_collection'
app.config['SESSION_KEY'] = 'very secret, do you believe?'
app.config['DEBUG'] = True
db = MongoAlchemy(app)

from forms import BookForm
from documents import Book
from views import *
