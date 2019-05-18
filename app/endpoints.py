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
