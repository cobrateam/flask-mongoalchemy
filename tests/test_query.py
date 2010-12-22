from tests import BaseTestCase
from tests.helpers import _make_todo_document
from flaskext import mongoalchemy
from flask import Flask

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

    def should_provide_a_get_or_404_method_on_query_object(self):
        "Should provide a \"get_or_404()\" method on Query object"
        abort = self.mocker.replace('flask.abort')
        abort(404)
        self.mocker.replay()
        searched_todo = self.Todo.query.get_or_404('9heuafahashoa8ehf')
        self.mocker.verify()
