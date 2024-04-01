#!/usr/bin/python3
"""
routes for handling state objects
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_states():
    """ gets all states """
    states = storage.all(State).values()
    formatted_states = [state.to_dict() for state in states]
    return jsonify(formatted_states)


@app_views.route("/states/<state_id>",  methods=["GET"], strict_slashes=False)
def get_state_by_id(state_id):
    """ get state by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                strict_slashes=False)
def delete_state_by_id(state_id):
    """delete state by id """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """ creates a new instance"""
    if not request.is_json:  #
        abort(400, 'Not a JSON')
    data = request.get_json()  #
    if 'name' not in data:
        abort(400, 'Missing name')
    new_state = State(**data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """ update states objs"""
    state_json = request.get_json(silent=True)
    if state_json is None:
        abort(400, 'Not a JSON')
    fetched_obj = storage.get(State, str(state_id))
    if fetched_obj is None:
        abort(404)
    for key, val in state_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(fetched_obj, key, val)
    fetched_obj.save()
    return jsonify(fetched_obj.to_dict()), 200
