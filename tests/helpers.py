# -*- coding: utf-8 -*-

# Copyright 2014 flask-mongoalchemy authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.


def _make_todo_document(db):
    class Todo(db.Document):
        description = db.StringField()
    return Todo
