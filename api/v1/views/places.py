#!/usr/bin/python3

"""view for place objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from flask import abort
from flask import jsonify
from flask import request
from flask import make_response
from models.user import User


@app_views.route("/cities/<string:city_id>/places", methods=['GET'],
                 strict_slashes=False)
def lisplaces(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    place = [obj.to_dict() for obj in city.places]
    return jsonify(place)


@app_views.route("/places/<place_id>", methods=['GET'],
                 strict_slashes=False)
def retrone(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=['DELETE'],
                 strict_slashes=False)
def delplace(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({})


@app_views.route("/cities/<city_id>/places", methods=['POST'],
                 strict_slashes=False)
def creplace(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'user_id' not in request.get_json():
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    user_id = request.get_json()['user_id']
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    request.get_json()['city_id'] = city_id
    new = Place(**request.get_json())
    new.save()
    return make_response(jsonify(new.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=["PUT"],
                 strict_slashes=False)
def updatepla(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in request.get_json().items():
        if key not in ['id', 'user_id', 'city_id', 'created_at'
                       'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict())
