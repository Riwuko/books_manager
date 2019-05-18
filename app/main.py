#!/usr/bin/env python3
from flask import Flask

from config import APP, DB
from endpoints import endpoint
from errors import error
from models import db

app = Flask(__name__)
app.register_blueprint(endpoint)
app.register_blueprint(error)

app.config[
    'SQLALCHEMY_DATABASE_URI'
] = f'postgresql+psycopg2://{DB.USER}:{DB.PASSWORD}@{DB.HOST}:{DB.PORT}/{DB.DBNAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = APP.SECRET_KEY

db.init_app(app)
