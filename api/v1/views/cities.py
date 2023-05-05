#!/usr/bin/python3

"""view for city objects to handle all default RESTFul API actions"""

from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from flask import abort
from flask import jsonify
from flask import request
from flask import make_response


@app_views.route("/states/<string:state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def allcity(state_id):
    """retrieves list of all city objects of a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    citie = [obj.to_dict() for obj in state.cities]
    return jsonify(citie)


@app_views.route("/cities/<string:city_id>", methods=["GET"],
                 strict_slashes=False)
def onecity(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<string:city_id>", methods=["DELETE"],
                 strict_slashes=False)
def delcity(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<string:state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def addcity(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    city = request.get_json()
    cite = City(**city)
    cite.state_id = state_id
    cite.save()
    return jsonify(cite.to_dict()), 201


@app_views.route("/cities/<string:city_id>", methods=["PUT"],
                 strict_slashes=False)
def updates(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    upd = request.get_json()
    for key, value in upd.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
