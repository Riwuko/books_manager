#!/usr/bin/env python3
"""Production config."""
import os


class APP:
    IP = "0.0.0.0"
    PORT = os.environ.get('APP_PORT')
    SECRET_KEY = os.environ.get('APP_SECRET_KEY')


class DB:
    USER = os.environ.get('DB_USER')
    PASSWORD = os.environ.get('DB_PASSWORD')
    HOST = os.environ.get('DB_HOST')
    PORT = os.environ.get('DB_PORT')
    DBNAME = os.environ.get('DB_NAME')

