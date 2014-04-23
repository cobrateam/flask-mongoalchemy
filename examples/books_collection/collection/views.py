# -*- coding: utf-8 -*-

# Copyright 2014 flask-mongoalchemy authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from flask import render_template, redirect, url_for

from collection import app
from collection.forms import BookForm
from collection.documents import Book


@app.route('/books/new', methods=['GET', 'POST'])
def new_book():
    form = BookForm()
    if form.validate_on_submit():
        form.save()
        return redirect(url_for('list_books'))
    return render_template('/books/new.html', form=form)


@app.route('/books')
@app.route('/books/<int:page>')
def list_books(page=1):
    title = u'Books list'
    pagination = Book.query.paginate(page=page, per_page=5)
    return render_template('/books/list_all.html', pagination=pagination, title=title)


@app.route('/books/<letter>')
@app.route('/books/<letter>/<int:page>')
def list_books_filtering(letter, page=1):
    title = u'Books starting with %s' % letter.upper()
    pagination = Book.query.starting_with(letter).paginate(page=page, per_page=5)
    return render_template('/books/list_filtered.html', pagination=pagination,
                           title=title, letter=letter)


@app.route('/books/delete/<id>')
def delete_book(id):
    book = Book.query.get_or_404(id)
    book.remove()
    return redirect(url_for('list_books'))


@app.route('/books/edit/<id>')
def edit_book(id):
    book = Book.query.get(id)
    form = BookForm(document=book)
    return render_template('/books/edit.html', form=form, book=book)


@app.route('/books/edit/<id>', methods=['POST'])
def update_book(id):
    book = Book.query.get(id)
    form = BookForm()
    if form.validate_on_submit():
        form.instance = book
        form.save()
        return redirect(url_for('list_books'))
    form = BookForm(document=book)
    return render_template('/books/edit.html', form=form, book=book)
