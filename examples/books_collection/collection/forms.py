from flaskext import wtf
from collection.documents import Book

class BookForm(wtf.Form):
    document_class = Book
    title = wtf.TextField(validators=[wtf.Required()])
    year = wtf.IntegerField(validators=[wtf.Required()])
    _instance = None

    def __init__(self, document=None, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        if document is not None:
            self._instance = document
            self._copy_data_to_form()

    def _copy_data_to_form(self):
        self.title.data = self._instance.title
        self.year.data = self._instance.year

    def save(self):
        if self._instance is None:
            self._instance = self.document_class()
        self._instance.title = self.title.data
        self._instance.year = self.year.data
        self._instance.save()
        return self._instance
