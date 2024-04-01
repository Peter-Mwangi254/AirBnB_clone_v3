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


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_city_by_id(city_id):
    '''Gets city by id'''
    city = storage.get(City, city_id)
    if not city:
        abort (404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"],
                strict_slashes=False)
def delete_a_city(city_id):
    """Deletes a city by id"""
    city = storage.get(City, city_id)
    if not city:
        abort (404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                strict_slashes=False)
def create_a_city(state_id):
    """Creates a city in State specified by the 'state_id' arg"""
    state = storage.get(State, state_id)
    if not state:
        abort (404)
    if not request.is_json:
        abort (400, 'Not a JSON')
    city_attrs = request.get_json()
    if 'name' not in city_attrs:
        abort (404, 'Missing name')
    new_city = City(**city_attrs)
    new_city.state_id = state_id # To set state_id attribute & column for city
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=['PUT'], strict_slashes=False)
def update_city_attributes(city_id):
    """Updates information about city specified by id"""
    city = storage.get(City, city_id)
    if not city:
        abort (404, 'No such city')
    if not request.is_json:
        abort (404, 'Not a JSON')
    data = request.get_json()
    for key, val in data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, val)
    city.save()
    return jsonify(city.to_dict()), 200
