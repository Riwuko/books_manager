"""SQLAlchemy tools."""
from models import Book, db


def bulk_add_books(books_to_add):
    """Add a large amount of books to database in one request.

    :param books_to_add: list of dicts with keys: title, author, category and description
    """
    for book in books_to_add:
        new_book = Book(**book)
        db.session.add(new_book)
    db.session.commit()


def filtering_books(column, value, exactly_match):
    """Helper function for custom filtering by user.

    :param column: selected column which books are filtered by e.g. title, author
    :param value: filter's value set by user
    :param exactly_match: value from checkbox on/off.
    If exactly_match equals 'on' the value of column must be exactly the same as the filter's value.
    If exactly_match equals anything else (off) the filer's value must be a part of column value.
    """
    if not value:
        return True
    if exactly_match == 'on':
        return column == value
    return column.ilike(f'%{value}%')


def get_books_by_title(books_titles):
    """Return all books with selected titles from database.

    :param books_titles: a list of book's titles
    """
    return Book.query.filter(Book.title.in_(books_titles)).all()


def get_filtered_books(page, filter_params):
    """Return selected, paginated books filtered by user.

    :param page: current page in pagination
    :param filter_params: dict with filtering query string parameters like title, author, category and exactly_match.
    """
    filter_title = filtering_books(Book.title, filter_params['title'], filter_params['exactly_match'])
    filter_author = filtering_books(Book.author, filter_params['author'], filter_params['exactly_match'])
    filter_category = filtering_books(Book.category, filter_params['category'], filter_params['exactly_match'])
    return (
        Book.query.filter(filter_title)
        .filter(filter_author)
        .filter(filter_category)
        .order_by(Book.title)
        .paginate(page, 8)
    )
