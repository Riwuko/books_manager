#!/usr/bin/env python3
from flask import Blueprint, flash, redirect, render_template, request, url_for

from models import Book, db
from sql_tools import bulk_add_books, get_books_by_title, get_filtered_books
from tools import import_books, prepare_new_books

endpoint = Blueprint('endpoint', __name__)


@endpoint.route('/')
def main_page():
    return render_template('index.html')


@endpoint.route('/import', methods=['GET', 'POST'])
def add_imported_books():
    """Import books from google and add them to database."""
    if request.method == 'GET':
        return render_template('books_import.html')
    elif request.method == 'POST':
        keyword = request.form.get('keyword')
        imported_books = import_books(keyword)
        imported_books_titles = {book['title'] for book in imported_books}
        existing_books = get_books_by_title(imported_books_titles)
        books_to_add = prepare_new_books(imported_books, existing_books)
        bulk_add_books(books_to_add)
        flash(f'Imported {len(books_to_add)} books. :)')
        return redirect(url_for('endpoint.add_imported_books'))


@endpoint.route('/new', methods=['GET', 'POST'])
def add_single_book():
    """Add single book to database."""
    if request.method == 'GET':
        return render_template('book_form.html')
    elif request.method == 'POST':
        form_data = {
            'author': request.form.get('author'),
            'title': request.form.get('title'),
            'category': request.form.get('category'),
            'description': request.form.get('description'),
        }
        existing_book = get_books_by_title(form_data['title'])
        if any(form_data['author'].lower() == selected.author.lower() for selected in existing_book):
            flash('This book already exists.')
            return redirect(url_for('endpoint.add_single_book'))
        new_book = Book(**form_data)
        db.session.add(new_book)
        db.session.commit()
        flash('Your book has been added.')
        return redirect(url_for('endpoint.add_single_book'))


@endpoint.route('/show', methods=['GET'])
def show_books():
    """Shows all books from database or if user set filters, only selected books."""
    page = request.args.get('page', 1, type=int)
    filter_params = {
        'title': request.args.get('title', None),
        'author': request.args.get('author', None),
        'category': request.args.get('category', None),
        'exactly_match': request.args.get('exactly_match', 'off').lower(),
    }
    return render_template(
        'books_list.html',
        books=get_filtered_books(page, filter_params),
        params={key: value for key, value in filter_params.items() if value},
    )
