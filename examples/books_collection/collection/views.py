from collection import app
from collection.forms import BookForm
from flask import render_template

@app.route('/books/new')
def new_book():
    form = BookForm()
    return render_template('/books/new.html', form=form)
