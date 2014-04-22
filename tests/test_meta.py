# -*- coding: utf-8 -*-

# Copyright 2010 flask-mongoalchemy authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from __future__ import absolute_import

from mongoalchemy import document

from flask.ext.mongoalchemy import Document
from flask.ext.mongoalchemy.meta import make_document_class
from tests import BaseAppTestCase


class MetaTestCase(BaseAppTestCase):
    "meta.py test case"

    def test_should_be_able_to_create_a_new_document(self):
        MyDocument = make_document_class(self.db, Document)
        assert issubclass(MyDocument, document.Document)
