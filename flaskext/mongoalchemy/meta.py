# -*- coding: utf-8 -*-
from __future__ import absolute_import

from flaskext.mongoalchemy import Document

from mongoalchemy import document


def make_document_class(session):
    class_dict = Document.__dict__.copy()
    class_dict.update({ '_session' : session })

    return type("Document", (document.Document,), class_dict)
