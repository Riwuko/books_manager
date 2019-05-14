#!/usr/bin/env python3
from flask import Blueprint
from flask import render_template

endpoint = Blueprint('endpoint', __name__)


@endpoint.route('/')
def main_page():
    return render_template('index.html')
