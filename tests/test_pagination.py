from tests import BaseTestCase
from tests.helpers import _make_todo_document
from flask import Flask
from werkzeug.exceptions import NotFound
from flaskext import mongoalchemy
from nose.tools import assert_equals, raises

class FlaskMongoAlchemyPaginationTestCase(BaseTestCase):
    "Flask-MongoAlchemy Pagination class"

    def setup(self):
        self.app = Flask(__name__)
        self.app.config['MONGOALCHEMY_DATABASE'] = 'testing'
        self.app.config['TESTING'] = True
        self.db = mongoalchemy.MongoAlchemy(self.app)
        self.Todo = _make_todo_document(self.db)

        # saving 30 Todo's
        for i in range(4, 34):
            todo = self.Todo(description=u'Write my %dth book' % i)
            todo.save()

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

    def should_provide_a_pages_property(self):
        pagination = self.Todo.query.filter({}).paginate(page=1)
        assert_equals(pagination.pages, 2)
        pagination = self.Todo.query.filter({}).paginate(page=1, per_page=50)
        assert_equals(pagination.pages, 1)

    def should_provide_a_has_next_method(self):
        "Should provide a \"has_next()\" method on Pagination object which returns True when there is a next page, and False when there is not"
        pagination = self.Todo.query.filter({}).paginate(page=1)
        assert pagination.has_next()
        pagination = self.Todo.query.filter({}).paginate(page=1, per_page=50)
        assert pagination.has_next() == False

    def should_provide_a_next_method(self):
        "Should provide a \"next()\" method on Pagination objects which returns a Pagination object for the next page"
        pagination = self.Todo.query.filter({}).paginate(page=1)
        next_page = pagination.next()
        assert_equals(next_page.page, 2)
        assert_equals(len(next_page.items), 10)

        self._replace_flask_abort()
        next_next_page = next_page.next(error_out=True)
        self.mocker.verify()

    def should_provide_a_has_prev_method(self):
        "Should provide a \"has_prev()\" method on Pagination object which returns True when there is a previous page, and False when there is not"
        pagination = self.Todo.query.filter({}).paginate(page=2)
        assert pagination.has_prev()
        pagination = self.Todo.query.filter({}).paginate(page=1, per_page=50)
        assert pagination.has_prev() == False
        pagination = self.Todo.query.filter({}).paginate(page=1)
        assert pagination.has_prev() == False

    @raises(NotFound)
    def should_provide_prev_method(self):
        "Should provide a \"prev()\" method on Pagination objects which returns a Pagination object for the previous page"
        pagination = self.Todo.query.filter({}).paginate(page=2)
        previous_page = pagination.prev()
        assert_equals(pagination.page, 2)
        assert_equals(previous_page.page, 1)
        assert_equals(len(previous_page.items), 20)

        self._replace_flask_abort_raising_exception()
        prev_prev_page = previous_page.prev(error_out=True)
        self.mocker.verify()

    def should_provide_the_number_of_the_next_page(self):
        pagination = self.Todo.query.filter({}).paginate(page=1)
        assert_equals(pagination.next_num, 2)
