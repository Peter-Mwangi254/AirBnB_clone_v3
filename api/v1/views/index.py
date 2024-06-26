#!/usr/bin/python3
"""
index
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.engine.file_storage import classes


@app_views.route('/status', strict_slashes=False)
def status():
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def get_total():
    tot_insts = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }

    return jsonify(tot_insts)
