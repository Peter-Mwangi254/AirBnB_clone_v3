#!/usr/bin/python3
"""
views module
"""
from flask import Blueprint
import states.py


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
