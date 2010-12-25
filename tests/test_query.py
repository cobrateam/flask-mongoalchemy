from tests import BaseTestCase
from tests.helpers import _make_todo_document
from flaskext import mongoalchemy
from flask import Flask
from werkzeug.exceptions import NotFound
from nose.tools import assert_equals, assert_raises

class FlaskMongoAlchemyQueryTestCase(BaseTestCase):
    "Flask-MongoAlchemy BaseQuery class"

    def setup(self):
        self.app = Flask(__name__)
        self.app.config['MONGOALCHEMY_DATABASE'] = 'testing'
        self.app.config['TESTING'] = True
        self.db = mongoalchemy.MongoAlchemy(self.app)
        self.Todo = _make_todo_document(self.db)

    def teardown(self):
        for todo in self.Todo.query.all():
            todo.remove()

    def _replace_flask_abort(self):
        """Replaces flask.abort function using mocker"""
        abort = self.mocker.replace('flask.abort')
        abort(404)
        self.mocker.replay()

    def _replace_flask_abort_raising_exception(self, calls=1):
        """Replaces flask.abort function using mocker"""
        abort = self.mocker.replace('flask.abort')
        abort(404)
        self.mocker.count(calls)
        self.mocker.throw(NotFound)
        self.mocker.replay()

    def should_provide_a_get_or_404_method_on_query_object(self):
        "Should provide a \"get_or_404()\" method on Query object"
        self._replace_flask_abort()
        searched_todo = self.Todo.query.get_or_404('9heuafahashoa8ehf')
        self.mocker.verify()

        todo = self.Todo(description=u'Start something')
        todo.save()
        searched_todo = self.Todo.query.get_or_404(todo.mongo_id)
        assert_equals(todo, searched_todo)

    def should_provide_a_first_or_404_method_on_query_object(self):
        "Should provide a \"first_or_404()\" method on Query object"
        self._replace_flask_abort()
        searched_todo = self.Todo.query.filter({}).first_or_404()
        self.mocker.verify()

        todo1 = self.Todo(description=u'Start something new')
        todo1.save()
        todo2 = self.Todo(description=u'Clean the room')
        todo2.save()
        searched_todo = self.Todo.query.filter({}).first_or_404()
        assert_equals(todo1, searched_todo)

    def should_provide_a_paginate_method_on_query_object(self):
        "Should provide a \"paginate()\" method on Query object which returns a Pagination object"
        for i in range(4, 20):
            todo = self.Todo(description=u'Try something for the %dth time' % i)
            todo.save()
        from flaskext.mongoalchemy import Pagination
        assert isinstance(self.Todo.query.paginate(page=1, per_page=5), Pagination)

    def should_abort_with_404_when_paginating_an_empty_query(self):
        "\"paginate()\" method should abort with 404 on empty result queries or when any parameter is wrong"
        todo = self.Todo(description=u'Do anything weird')
        todo.save()

        self._replace_flask_abort_raising_exception(calls=2)
        assert_raises(NotFound, self.Todo.query.filter({u'description' : u'Do anything weird'}).paginate, page=2)
        assert_raises(NotFound, self.Todo.query.filter({u'description' : u'Do anything good'}).paginate, page=0)
        self.mocker.verify()
