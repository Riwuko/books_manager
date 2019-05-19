#!/usr/bin/env python3
"""Production config."""
import os
import re


class APP:
    IP = "0.0.0.0"
    SECRET_KEY = os.environ.get('APP_SECRET_KEY')


class DB:
    HEROKU_DB_URL = re.search(
        r'\/\/(?P<user>\w+):(?P<password>\w+)@(?P<host>[\w\.\-]+):(?P<port>\w+)\/(?P<dbname>\w+)',
        os.environ.get('DATABASE_URL'),
    )
    USER = HEROKU_DB_URL.group('user')
    PASSWORD = HEROKU_DB_URL.group('password')
    HOST = HEROKU_DB_URL.group('host')
    PORT = HEROKU_DB_URL.group('port')
    DBNAME = HEROKU_DB_URL.group('dbname')
