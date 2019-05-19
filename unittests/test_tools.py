from unittest.mock import Mock, patch

import pytest

from app.tools import import_books


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
