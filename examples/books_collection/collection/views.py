from collection import app
from collection.forms import BookForm
from collection.documents import Book
from flask import render_template, redirect, url_for

@app.route('/books/new', methods=['GET', 'POST'])
def new_book():
    form = BookForm()
    if form.validate_on_submit():
        form.save()
        return redirect(url_for('list_books'))
    return render_template('/books/new.html', form=form)

@app.route('/books')
def list_books():
    books = Book.query.all()
    return render_template('/books/list.html', books=books)

@app.route('/books/delete/<id>')
def delete_book(id):
    book = Book.query.get_or_404(id)
    book.remove()
    return redirect(url_for('list_books'))

@app.route('/books/edit/<id>')
def edit_book(id):
    book = Book.get(id)
    form = BookForm(document=book)
    return render_template('/books/edit.html', form=form, book=book)

@app.route('/books/edit/<id>', methods=['POST'])
def update_book(id):
    book = Book.get(id)
    form = BookForm()
    if form.validate_on_submit():
        form.instance = book
        form.save()
        return redirect(url_for('list_books'))
    form = BookForm(document=book)
    return render_template('/books/edit.html', form=form, book=book)
