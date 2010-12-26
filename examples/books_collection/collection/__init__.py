from flask import Flask
from flaskext.mongoalchemy import MongoAlchemy
import string

app = Flask(__name__)
app.config['MONGOALCHEMY_DATABASE'] = 'books_collection'
app.config['SECRET_KEY'] = 'very secret, do you believe?'
app.config['DEBUG'] = True
db = MongoAlchemy(app)

@app.context_processor
def put_letters_on_request():
    return { 'letters' : string.ascii_uppercase }

from views import *
