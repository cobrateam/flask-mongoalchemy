# -*- coding: utf-8 -*-

# Copyright 2014 flask-mongoalchemy authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import flask_mongoalchemy as mongoalchemy
from mocker import MockerTestCase
from flask import Flask
from werkzeug.exceptions import NotFound
from tests.helpers import _make_todo_document


class BaseTestCase(MockerTestCase):

    def setUp(self):
        super(BaseTestCase, self).setUp()
        self.setup()

    def tearDown(self):
        super(BaseTestCase, self).tearDown()
        self.teardown()

    def setup(self):
        pass

    def teardown(self):
        pass


class BaseAppTestCase(BaseTestCase):

    def setup(self):
        self.app = Flask(__name__)
        self.app.config['MONGOALCHEMY_DATABASE'] = 'testing'
        self.app.config['TESTING'] = True
        self.db = mongoalchemy.MongoAlchemy(self.app)
        self.Todo = _make_todo_document(self.db)

    def teardown(self):
        for todo in self.Todo.query.all():
            todo.remove()

    def _replace_flask_abort(self, calls=1):
        """Replaces flask.abort function using mocker"""
        abort = self.mocker.replace('flask.abort')
        abort(404)
        self.mocker.count(calls)
        self.mocker.replay()

    def _replace_flask_abort_raising_exception(self, calls=1):
        """Replaces flask.abort function using mocker"""
        abort = self.mocker.replace('flask.abort')
        abort(404)
        self.mocker.count(calls)
        self.mocker.throw(NotFound)
        self.mocker.replay()
