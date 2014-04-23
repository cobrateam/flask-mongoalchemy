# -*- coding: utf-8 -*-

# Copyright 2014 flask-mongoalchemy authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from flask import Flask
from flask.ext.mongoalchemy import MongoAlchemy
import string

app = Flask(__name__)
app.config['MONGOALCHEMY_DATABASE'] = 'books_collection'
app.config['SECRET_KEY'] = 'very secret, do you believe?'
app.config['DEBUG'] = True
db = MongoAlchemy(app)


@app.context_processor
def put_letters_on_request():
    return {'letters': string.ascii_uppercase}

import views
_ = views
