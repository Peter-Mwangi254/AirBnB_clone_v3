#!/usr/bin/python3

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State

@app_views.route("/states", methods=['GET'])
def get_states():
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route("/states/<state_id>",  methods=["GET"])
def get_state_by_id(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_state_by_id(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({})


@app_views.route("/states", methods=["POST"])
def create_state():
    if not request.json:
        abort(400, 'Not a JSON')
    if 'name' not in request.json:
        abort(400, 'Missing name')
    data = request.json
    new_state = State(**data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>",  methods=["PUT"])
def update_state(state_id):
    state_json = request.get_json(silent=True)
    if state_json is None:
        abort(400, 'Not a JSON')
    fetched_obj = storage.get("State", str(state_id))
    if fetched_obj is None:
        abort(404)
    for key, val in state_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(fetched_obj, key, val)
    fetched_obj.save()
    return jsonify(fetched_obj.to_json())
