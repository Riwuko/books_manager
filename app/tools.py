"""Miscellaneous tools."""
import requests


def import_books(keyword):
    """Make a request to google api and get books by keyword.

    :param keyword: parameter 'q' in request to google api
    """
    resp_books = (
        requests.get('https://www.googleapis.com/books/v1/volumes', params={'q': keyword, 'maxResults': 40})
        .json()
        .get('items', [])
    )
    return [
        {
            'author': ', '.join(book['volumeInfo'].get('authors', [])),
            'title': book['volumeInfo'].get('title', ''),
            'category': ', '.join(book['volumeInfo'].get('categories', [])),
            'description': book['volumeInfo'].get('description', ''),
        }
        for book in resp_books
    ]


def prepare_new_books(imported_books, existing_books):
    """Prepare books to add to database without repetition (existing books in database).

    :param imported_books: list with dictionaries with informations about all imported books
    :param existin_books: list of Books database objects
    """
    return [
        new_book
        for new_book in imported_books
        if not any(
            # remove books which are in database already
            new_book['author'].lower() == existing_book.author.lower()
            and new_book['title'].lower() == existing_book.title.lower()
            for existing_book in existing_books
        )
    ]
