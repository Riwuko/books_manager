#!/usr/bin/env python3
from flask import Flask

from endpoints import endpoint
from errors import error

app = Flask(__name__)
app.register_blueprint(endpoint)
app.register_blueprint(error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
