#!/usr/bin/env python3
from flask import Blueprint, render_template

error = Blueprint('error', __name__)


@error.app_errorhandler(404)
def page_not_found(e):
    return render_template('not_found.html'), 404
