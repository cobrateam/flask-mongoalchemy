from tests import BaseTestCase
from tests.helpers import _make_todo_document
from flaskext import mongoalchemy
from flask import Flask
from nose.tools import assert_equals

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
        "Should provide a \"paginate()\" method on Query object"
        assert False
