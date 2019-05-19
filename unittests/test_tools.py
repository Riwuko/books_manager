from unittest.mock import Mock, patch

import pytest

from app.tools import import_books, prepare_new_books


class GoogleResponse:
    def __init__(self, response):
        self.response = response

    def json(self):
        return self.response


@pytest.mark.parametrize(
    'response, output',
    (
        ({}, []),
        (
            {
                'items': [
                    {
                        'volumeInfo': {
                            'authors': ['John', 'Mike'],
                            'title': 'something',
                            'categories': ['fantasy', 'horror'],
                            'description': 'some description',
                        }
                    }
                ]
            },
            [
                {
                    'author': 'John, Mike',
                    'title': 'something',
                    'category': 'fantasy, horror',
                    'description': 'some description',
                }
            ],
        ),
        (
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
            [
                {
                    'author': 'John, Mike',
                    'title': 'something',
                    'category': 'fantasy, horror',
                    'description': 'some description',
                },
                {'author': 'Amy', 'title': 'something else', 'category': 'fiction', 'description': 'space'},
            ],
        ),
    ),
)
def test_import_books(response, output):
    with patch('tools.requests.get', Mock(return_value=GoogleResponse(response))):
        assert import_books('keyword') == output


class ExistingBook:
    def __init__(self, author, title):
        self.author = author
        self.title = title


@pytest.mark.parametrize(
    'imported_books, existing_books_params, expected_output',
    (
        (
            [
                {
                    'author': 'John, Mike',
                    'title': 'something',
                    'category': 'fantasy, horror',
                    'description': 'some description',
                },
                {
                    'author': 'Amy',
                    'title': 'something else',
                    'category': 'fiction',
                    'description': 'space around the earth',
                },
            ],
            [('Amy', 'something else'), ('John, Mike', 'bbb'), ('Someone', 'something')],
            [
                {
                    'author': 'John, Mike',
                    'title': 'something',
                    'category': 'fantasy, horror',
                    'description': 'some description',
                }
            ],
        ),
        (
            [
                {
                    'author': 'John, Mike',
                    'title': 'something',
                    'category': 'fantasy, horror',
                    'description': 'some description',
                },
                {
                    'author': 'Amy',
                    'title': 'something else',
                    'category': 'fiction',
                    'description': 'space around the earth',
                },
            ],
            [('Amy', 'something else'), ('John, Mike', 'bbb'), ('Someone', 'something'), ('John, Mike', 'something')],
            [],
        ),
        (
            [
                {
                    'author': 'John, Mike',
                    'title': 'something',
                    'category': 'fantasy, horror',
                    'description': 'some description',
                },
                {
                    'author': 'Amy',
                    'title': 'something else',
                    'category': 'fiction',
                    'description': 'space around the earth',
                },
            ],
            [
                ('Amy', 'something else2'),
                ('John, Mike', 'bbb'),
                ('Someone', 'something'),
                ('John, Mike', 'something22'),
            ],
            [
                {
                    'author': 'John, Mike',
                    'title': 'something',
                    'category': 'fantasy, horror',
                    'description': 'some description',
                },
                {
                    'author': 'Amy',
                    'title': 'something else',
                    'category': 'fiction',
                    'description': 'space around the earth',
                },
            ],
        ),
    ),
)
def test_prepare_new_books(imported_books, existing_books_params, expected_output):
    existing_books = [ExistingBook(*params) for params in existing_books_params]
    assert prepare_new_books(imported_books, existing_books) == expected_output
