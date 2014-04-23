# -*- coding: utf-8 -*-

# Copyright 2014 flask-mongoalchemy authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import wtforms
from flask.ext import wtf
from wtforms import validators

from collection.documents import Book


class BookForm(wtf.Form):
    document_class = Book
    title = wtforms.TextField(validators=[validators.Required()])
    year = wtforms.IntegerField(validators=[validators.Required()])
    instance = None

    def __init__(self, document=None, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        if document is not None:
            self.instance = document
            self._copy_data_to_form()

    def _copy_data_to_form(self):
        self.title.data = self.instance.title
        self.year.data = self.instance.year

    def save(self):
        if self.instance is None:
            self.instance = self.document_class()
        self.instance.title = self.title.data
        self.instance.year = self.year.data
        self.instance.save()
        return self.instance
