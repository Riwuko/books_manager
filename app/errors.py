#!/usr/bin/env python3
from flask import Blueprint

error = Blueprint('error', __name__)


@error.app_errorhandler(404)
def page_not_found(e):
    return 'Not Found', 404
