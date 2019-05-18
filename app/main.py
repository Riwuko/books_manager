#!/usr/bin/env python3
from flask import Flask

from endpoints import endpoint
from errors import error
from models import db

app = Flask(__name__)
app.register_blueprint(endpoint)
app.register_blueprint(error)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///foo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'abc'

db.init_app(app)
