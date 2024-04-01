#!/usr/bin/python3
"""
views module
"""
from flask import Blueprint
# from ....models.states import *


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
