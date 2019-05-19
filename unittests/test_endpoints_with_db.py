import os

import pytest

from app.main import app
from app.models import db
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
