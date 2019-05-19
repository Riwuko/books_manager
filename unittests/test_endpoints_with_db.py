import os
from unittest.mock import Mock, patch

import pytest

from app.main import app
from app.models import Book, db
from unittest_tools.unittest_objects import GoogleResponse
from unittest_tools.unittest_tools import flask_response_data

TEST_DATABASE_URI = 'sqlite:///test_project.db'


@pytest.fixture
def app_fixture():
    app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DATABASE_URI
    app.config['TESTING'] = True
    client = app.test_client()
    with app.app_context():
        db.init_app(app)
    app.app_context().push()
    db.create_all()
    yield client
    os.remove("app/test_project.db")


@pytest.mark.parametrize(
    'sql_values, query_string, status_code, resp_data',
    (
        (
            '("The Hobbit", "Tolkien", "Fantasy", "Long journey")',
            '',
            200,
            "<tr><td>The Hobbit</td><td>Tolkien</td><td>Fantasy</td><td>Long journey</td></tr>",
        ),
        (
            '''
            ("The Hobbit", "Tolkien", "Fantasy", "Long journey"),
            ("Book1", "Author1", "Sth", "Descr"),
            ("Book2", "Author1", "Sth", "Descr"),
            ("Book3", "Author1", "Sth", "Descr"),
            ("Book4", "Author1", "Sth", "Descr"),
            ("Book5", "Author1", "Sth", "Descr"),
            ("Book6", "Author1", "Sth", "Descr"),
            ("Book7", "Author1", "Sth", "Descr"),
            ("Book8", "Author1", "Sth", "Descr")
            ''',
            '',
            200,
            '''
            <tr><td>Book1</td><td>Author1</td><td>Sth</td><td>Descr</td></tr>
            <tr><td>Book2</td><td>Author1</td><td>Sth</td><td>Descr</td></tr>
            <tr><td>Book3</td><td>Author1</td><td>Sth</td><td>Descr</td></tr>
            <tr><td>Book4</td><td>Author1</td><td>Sth</td><td>Descr</td></tr>
            <tr><td>Book5</td><td>Author1</td><td>Sth</td><td>Descr</td></tr>
            <tr><td>Book6</td><td>Author1</td><td>Sth</td><td>Descr</td></tr>
            <tr><td>Book7</td><td>Author1</td><td>Sth</td><td>Descr</td></tr>
            <tr><td>Book8</td><td>Author1</td><td>Sth</td><td>Descr</td></tr>
            ''',
        ),
        (
            '''
            ("The Hobbit", "Tolkien", "Fantasy", "Long journey"),
            ("Book1", "Author1", "Sth", "Descr"),
            ("Book2", "Author1", "Sth", "Descr"),
            ("Book3", "Author1", "Sth", "Descr"),
            ("Book4", "Author1", "Sth", "Descr"),
            ("Book5", "Author1", "Sth", "Descr"),
            ("Book6", "Author1", "Sth", "Descr"),
            ("Book7", "Author1", "Sth", "Descr"),
            ("Book8", "Author1", "Sth", "Descr")
            ''',
            'page=2',
            200,
            '<tr><td>The Hobbit</td><td>Tolkien</td><td>Fantasy</td><td>Long journey</td></tr>',
        ),
        (
            '''
            ("The Hobbit", "Tolkien", "Fantasy", "Long journey"),
            ("Book1", "Author1", "Sth", "Descr"),
            ("Book2", "Author1", "Sth", "Descr"),
            ("Book3", "Author2", "Sth", "Descr"),
            ("Book4", "Author2", "Sth", "Descr"),
            ("Book5", "Author3", "Sth", "Descr"),
            ("Book6", "Author3", "Sth", "Descr"),
            ("Book7", "Author3", "Sth", "Descr"),
            ("Book8", "Author4", "Sth", "Descr")
            ''',
            'author=hor1',
            200,
            '''
            <tr><td>Book1</td><td>Author1</td><td>Sth</td><td>Descr</td></tr>
            <tr><td>Book2</td><td>Author1</td><td>Sth</td><td>Descr</td></tr>
            ''',
        ),
        (
            '''
            ("The Hobbit", "Tolkien", "Fantasy", "Long journey"),
            ("Book1", "Author1", "Sth", "Descr"),
            ("Book2", "Author1", "Sth", "Descr"),
            ("Book3", "Author2", "Sth", "Descr"),
            ("Book4", "Author2", "Sth", "Descr"),
            ("Book5", "Author3", "Sth", "Descr"),
            ("Book6", "Author3", "Sth", "Descr"),
            ("Book7", "Author3", "Sth", "Descr"),
            ("Book8", "Author4", "Sth", "Descr")
            ''',
            'author=Author1&exactly_match=on',
            200,
            '''
            <tr><td>Book1</td><td>Author1</td><td>Sth</td><td>Descr</td></tr>
            <tr><td>Book2</td><td>Author1</td><td>Sth</td><td>Descr</td></tr>
            ''',
        ),
        (
            '''
            ("The Hobbit", "Tolkien", "Fantasy", "Long journey"),
            ("Book1", "Author1", "Sth", "Descr"),
            ("Book2", "Author1", "Sth", "Descr"),
            ("Book3", "Author2", "Sth", "Descr"),
            ("Book4", "Author2", "Sth", "Descr"),
            ("Book5", "Author3", "Sth", "Descr"),
            ("Book6", "Author3", "Sth", "Descr"),
            ("Book7", "Author3", "Sth", "Descr"),
            ("Book8", "Author4", "Sth", "Descr")
            ''',
            'category=fant',
            200,
            '<tr><td>The Hobbit</td><td>Tolkien</td><td>Fantasy</td><td>Long journey</td></tr>',
        ),
        (
            '''
            ("The Hobbit", "Tolkien", "Fantasy", "Long journey"),
            ("Book1", "Author1", "Sth", "Descr"),
            ("Book2", "Author1", "Sth", "Descr"),
            ("Book3", "Author2", "Sth", "Descr"),
            ("Book4", "Author2", "Sth", "Descr"),
            ("Book5", "Author3", "Sth", "Descr"),
            ("Book6", "Author3", "Sth", "Descr"),
            ("Book7", "Author3", "Sth", "Descr"),
            ("Book8", "Author4", "Sth", "Descr"),
            ("Book9", "Author4", "Sth", "Descr")
            ''',
            'title=book&page=2',
            200,
            '<tr><td>Book9</td><td>Author4</td><td>Sth</td><td>Descr</td></tr>',
        ),
    ),
)
def test_show_books_endpoint(app_fixture, sql_values, query_string, status_code, resp_data):
    db.engine.execute(f'INSERT INTO books (title, author, category, description) VALUES {sql_values}')
    resp = app_fixture.get(f'/show?{query_string}')
    assert resp.status_code == status_code
    assert "".join(resp_data.split()) in flask_response_data(resp)


@pytest.mark.parametrize(
    'sql_values, response, added_count, total_db',
    (
        (
            '("Book1", "Author1", "Sth", "Descr")',
            {
                'items': [
                    {
                        'volumeInfo': {
                            'authors': ['John', 'Mike'],
                            'title': 'something',
                            'categories': ['fantasy', 'horror'],
                            'description': 'some description',
                        }
                    },
                    {
                        'volumeInfo': {
                            'authors': ['Amy'],
                            'title': 'something else',
                            'categories': ['fiction'],
                            'description': 'space',
                        }
                    },
                ]
            },
            2,
            3,
        ),
        (
            '("something else", "Amy", "fiction", "space")',
            {
                'items': [
                    {
                        'volumeInfo': {
                            'authors': ['John', 'Mike'],
                            'title': 'something',
                            'categories': ['fantasy', 'horror'],
                            'description': 'some description',
                        }
                    },
                    {
                        'volumeInfo': {
                            'authors': ['Amy'],
                            'title': 'something else',
                            'categories': ['fiction'],
                            'description': 'space',
                        }
                    },
                ]
            },
            1,
            2,
        ),
    ),
)
def test_add_imported_books_endpoint(app_fixture, sql_values, response, added_count, total_db):
    db.engine.execute(f'INSERT INTO books (title, author, category, description) VALUES {sql_values}')
    with patch('tools.requests.get', Mock(return_value=GoogleResponse(response))):
        resp = app_fixture.post('/import', data={'keyword': 'keyword'}, follow_redirects=True)

    assert resp.status_code == 200
    assert ''.join(f'Imported {added_count} books. :)'.split()) in flask_response_data(resp)
    assert db.session.query(Book).count() == total_db
