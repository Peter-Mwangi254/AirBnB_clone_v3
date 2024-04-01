#!/usr/bin/python3
"""
routes for handling operations on Place objects"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City


@app_views.route("cities/<city_id>/places", methods=['GET'],
                strict_slashes=False)
def get_all_places(city_id):
    """ all Place objects by city """
    city = storage.get(City, city_id)
    if not city:
        return abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route("/places/<place_id>",  methods=["GET"],
                 strict_slashes=False)
def get_place(place_id):
    """retrive place object by place_id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>",  methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id):
    """deletes Place by id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def create_place(city_id):
    """creates a place object"""
    city = storage.get(City, city_id)
    if not city:
        return abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    data = request.get_json
    if not request.get_json():
        abort(400, "Missing user_id")
    if 'name' not in data:
        abort(400, "Missing name")
    user = storage.get(User, data['user_id'])
    if not user:
        return abort(404)
    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>",  methods=["PUT"],
                 strict_slashes=False)
def update_place(place_id):
    """ updates specific Place object by ID """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
