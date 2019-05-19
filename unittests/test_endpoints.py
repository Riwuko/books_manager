#!/usr/bin/env python3
import pytest

from app.main import app
from unittest_tools.unittest_tools import flask_response_data


@pytest.fixture()
def app_fixture():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client


@pytest.mark.parametrize(
    'url_path, status_code, resp_data',
    (
        (
            '/',
            200,
            """
            <a href='/import'>Import books</a>
            <a href='/new'>Add single new book</a>
            <a href='/show'>Show books</a>
            """,
        ),
        ('/wrong/url/path', 404, 'Not Found'),
        (
            '/import',
            200,
            '''
         <a href='/'>Main Page</a>
                Import from google by keyword:
                <form method="post">
                    <input type="text" name="keyword" placeholder="Keyword"/>
                    <button type="submit">Submit</button>
                </form>
            ''',
        ),
        (
            '/new',
            200,
            '''
            <a href='/'>Main Page</a>
                <form method="post">
                    <input type="text" name="title" placeholder="Book's title"/>
                    <input type="text" name="author" placeholder="Author"/>
                    <input type="text" name="category" placeholder="Category"/>
                    <input type="text" name="description" placeholder="Description"/>
                    <button type="submit">Submit</button>
                </form>
            ''',
        ),
    ),
)
def test_simple_endpoint(app_fixture, url_path, status_code, resp_data):
    resp = app_fixture.get(url_path)
    assert resp._status_code == status_code
    assert "".join(resp_data.split()) in flask_response_data(resp)
