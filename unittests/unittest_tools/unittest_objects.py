class ExistingBook:
    def __init__(self, author, title):
        self.author = author
        self.title = title


class GoogleResponse:
    def __init__(self, response):
        self.response = response

    def json(self):
        return self.response
