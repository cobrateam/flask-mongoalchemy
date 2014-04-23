# -*- coding: utf-8 -*-

# Copyright 2014 flask-mongoalchemy authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from mongoalchemy import document


def make_document_class(session, document_class):
    class_dict = document_class.__dict__.copy()
    class_dict.update({'_session': session})
    return type("Document", (document.Document,), class_dict)
