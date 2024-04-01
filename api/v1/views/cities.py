#!/usr/bin/python3
"""
routes for handling cities objects
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET"], strict_slashes=False)
def get_cities(state_id):
    """ gets all cities by state id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    list_cities = [city.to_dict() for city in state.cities]
    return jsonify(list_cities)
