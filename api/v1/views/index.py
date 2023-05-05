#!/usr/bin/python3
"""create a route status"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def status():
    """json status on"""
    status = {"status": "OK"}
    return jsonify(status)


@app_views.route("/stats")
def count():
    """endpoint retrieves number of each object by type"""
    classes = {"amenities": storage.count("Amenity"),
               "cities": storage.count("City"),
               "places": storage.count("Place"),
               "reviews": storage.count("Review"),
               "states": storage.count("State"),
               "users": storage.count("User")
               }
    return jsonify(classes)
