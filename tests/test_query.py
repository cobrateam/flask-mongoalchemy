# -*- coding: utf-8 -*-

# Copyright 2010 flask-mongoalchemy authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from tests import BaseAppTestCase
from werkzeug.exceptions import NotFound


class FlaskMongoAlchemyQueryTestCase(BaseAppTestCase):
    "Flask-MongoAlchemy BaseQuery class"

    def test_should_provide_a_get_method_on_query_object(self):
        "Should provide a \"get()\" method on Query object"
        todo = self.Todo(description=u'Start something very new')
        todo.save()
        searched_todo = self.Todo.query.get(str(todo.mongo_id))
        self.assertEqual(todo, searched_todo)

    def test_should_return_None_when_querying_for_a_non_existing_document_on_database(self):
        "\"get()\" method should return None when querying for a non-existing document"
        searched_todo = self.Todo.query.get('4e038a23e4206650da0000df')
        assert searched_todo is None

    def test_should_provide_a_get_or_404_method_on_query_object(self):
        "Should provide a \"get_or_404()\" method on Query object"
        self._replace_flask_abort()
        searched_todo = self.Todo.query.get_or_404('4e038a23e4206650da0000df')
        self.mocker.verify()

        todo = self.Todo(description=u'Start something')
        todo.save()
        searched_todo = self.Todo.query.get_or_404(str(todo.mongo_id))
        self.assertEqual(todo, searched_todo)

    def test_should_provide_a_first_or_404_method_on_query_object(self):
        "Should provide a \"first_or_404()\" method on Query object"
        self._replace_flask_abort()
        searched_todo = self.Todo.query.filter({}).first_or_404()
        self.mocker.verify()

        todo1 = self.Todo(description=u'Start something new')
        todo1.save()
        todo2 = self.Todo(description=u'Clean the room')
        todo2.save()
        searched_todo = self.Todo.query.filter({}).first_or_404()
        self.assertEqual(todo1, searched_todo)

    def test_should_provide_a_paginate_method_on_query_object(self):
        for i in range(4, 20):
            todo = self.Todo(description=u'Try something for the %dth time' % i)
            todo.save()
        from flask.ext.mongoalchemy import Pagination
        assert isinstance(self.Todo.query.paginate(page=1, per_page=5), Pagination)

    def test_should_abort_with_404_when_paginating_an_empty_query(self):
        todo = self.Todo(description=u'Do anything weird')
        todo.save()

        self._replace_flask_abort_raising_exception(calls=2)
        self.assertRaises(NotFound,
                          self.Todo.query.filter(self.Todo.description ==
                                                 u'Do anything weird').paginate, page=2)
        self.assertRaises(NotFound,
                          self.Todo.query.filter(self.Todo.description ==
                                                 u'Do anything good').paginate, page=0)
        self.mocker.verify()

    def test_should_return_None_for_wrong_formated_objectids(self):
        todo = self.Todo.query.get("blasphemy")
        assert todo is None
