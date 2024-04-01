#!/usr/bin/python3
'''
routes for handling operations on Amenity objects'''
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", strict_slashes=False)
def get_amenities():
    '''Retrieves the list of all Amenity objects'''
    amenities = storage.all(Amenity).values()
    dict_amenities = [amenity.to_dict() for amenity in amenities]
    return jsonify(dict_amenities)


@app_views.route("/amenities/<amenity_id>", strict_slashes=False)
def get_amenities_id(amenity_id):
    '''Retrieves an amenity object by id'''
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort (404, 'Input valid amenity')
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'],
                strict_slashes=False)
def delete_amenity(amenity_id):
    '''Delete an amenity by ID'''
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort (404, 'Could not find amenity')
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods=['POST'], strict_slashes=False)
def create_amenity():
    '''Creates new amenity object'''
    if not request.is_json:
        abort (400, 'Not a JSON')
    amenity_data = response.get_json()
    if 'name' not in amenity_data:
        abort(404, 'Missing name')
    new_amen = Amenity(**amenity_data)
    storage.new(new_amen)
    storage.save()
    return jsonify(new_amen.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    '''Updates amenity by Id'''
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort (404, 'Invalid amenity')
    if not response.is_json:
        abort(404, 'Not a JSON')
    amenity_attrs = response.get_json()
    for k, v in amenity_attrs.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, k, v)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
