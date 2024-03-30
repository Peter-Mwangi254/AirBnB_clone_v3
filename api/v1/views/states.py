#!/usr/bin/python3

from api.v1.views import app_views
from flask import jsonify
from models import storage

@app.route("/state", method=['GET'])
def get_states():
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app.route("/states/<state_id>",  methods=["GET"])
def get_state_by_id(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app.route("/states/<state_id>", methods=["DELETE"])
def delete_state_by_id(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({})


@app.route("/states", methods=["POST"])
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
