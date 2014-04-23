# -*- coding: utf-8 -*-

# Copyright 2010 flask-mongoalchemy authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from tests import BaseAppTestCase
from werkzeug.exceptions import NotFound


class FlaskMongoAlchemyPaginationTestCase(BaseAppTestCase):
    "Flask-MongoAlchemy Pagination class"

    def setup(self):
        super(FlaskMongoAlchemyPaginationTestCase, self).setup()

        # saving 30 Todo's
        for i in range(4, 34):
            todo = self.Todo(description=u'Write my %dth book' % i)
            todo.save()

    def test_should_provide_a_pages_property(self):
        pagination = self.Todo.query.filter({}).paginate(page=1)
        self.assertEqual(pagination.pages, 2)
        pagination = self.Todo.query.filter({}).paginate(page=1, per_page=50)
        self.assertEqual(pagination.pages, 1)

    def test_should_provide_a_has_next_method(self):
        pagination = self.Todo.query.filter({}).paginate(page=1)
        assert pagination.has_next()
        pagination = self.Todo.query.filter({}).paginate(page=1, per_page=50)
        assert pagination.has_next() is False

    def test_should_provide_a_next_method(self):
        pagination = self.Todo.query.filter({}).paginate(page=1)
        next_page = pagination.next()
        self.assertEqual(next_page.page, 2)
        self.assertEqual(len(next_page.items), 10)
        self._replace_flask_abort()
        next_page.next(error_out=True)
        self.mocker.verify()

    def test_should_provide_a_has_prev_method(self):
        pagination = self.Todo.query.filter({}).paginate(page=2)
        assert pagination.has_prev()
        pagination = self.Todo.query.filter({}).paginate(page=1, per_page=50)
        assert pagination.has_prev() is False
        pagination = self.Todo.query.filter({}).paginate(page=1)
        assert pagination.has_prev() is False

    def test_should_provide_prev_method(self):
        pagination = self.Todo.query.filter({}).paginate(page=2)
        previous_page = pagination.prev()
        self.assertEqual(pagination.page, 2)
        self.assertEqual(previous_page.page, 1)
        self.assertEqual(len(previous_page.items), 20)
        with self.assertRaises(NotFound):
            self._replace_flask_abort_raising_exception()
            previous_page.prev(error_out=True)
            self.mocker.verify()

    def test_should_provide_the_number_of_the_next_page(self):
        pagination = self.Todo.query.filter({}).paginate(page=1)
        self.assertEqual(pagination.next_num, 2)

    def test_should_provide_the_number_of_the_previous_page(self):
        pagination = self.Todo.query.filter({}).paginate(page=2)
        self.assertEqual(pagination.prev_num, 1)
