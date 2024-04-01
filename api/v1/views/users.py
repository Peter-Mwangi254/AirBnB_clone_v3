#!/usr/bin/python3
"""
This file contains the User module
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_users():
    """ gets all states """
    users = storage.all(User).values()
    dict_users = [user.to_dict() for user in users]
    return jsonify(dict_users)


@app_views.route("/users/<user_id>", methods=['GET'], strict_slashes=False)
def get_users(user_id):
    """Retrieves an user object by id"""
    user = storage.get(User, user_id)
    if not user:
        abort (404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=['DELETE'],
                strict_slashes=False)
def delete_user(user_id):
    '''Delete a user by ID'''
    user = storage.get(User, user_id)
    if not user:
        abort (404)
    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=['POST'], strict_slashes=False)
def create_user():
    """Creates new user object"""
    if not request.is_json:
        abort (400, 'Not a JSON')
    user_data = request.get_json()
    if 'email' not in user_data:
        abort(400, 'Missing email')
    if 'password' not in user_data:
        abort(400, 'Missing password')
    new_user = User(**user_data)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates user by Id"""
    user = storage.get(User, user_id)
    if not user:
        abort (404, 'Invalid user')
    if not response.is_json:
        abort(400, 'Not a JSON')
    user_attrs = request.get_json()
    for k, v in user_attrs.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(user, k, v)
    user.save()
    return jsonify(user.to_dict()), 200
