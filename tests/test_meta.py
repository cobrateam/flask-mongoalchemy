# -*- coding: utf-8 -*-
from __future__ import absolute_import

from mongoalchemy import document

from flaskext.mongoalchemy.meta import make_document_class
from tests import BaseAppTestCase


class MetaTestCase(BaseAppTestCase):
    "meta.py test case"

    def should_be_able_to_create_a_new_document(self):
        Document = make_document_class(self.db)
        assert issubclass(Document, document.Document)
