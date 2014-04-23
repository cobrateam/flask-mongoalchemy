# -*- coding: utf-8 -*-

# Copyright 2014 flask-mongoalchemy authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from collection import db
from flask.ext.mongoalchemy import BaseQuery
import re


class BookQuery(BaseQuery):

    def starting_with(self, letter):
        regex = r'^' + letter
        return self.filter({'title': re.compile(regex, re.IGNORECASE)})


class Book(db.Document):
    query_class = BookQuery

    title = db.StringField()
    year = db.IntField()
