#!/usr/bin/python3

"""views for amenity objects handles default RESTFul API actions"""

from models import storage
from models.amenity import Amenity
from flask import request
from flask import jsonify
from api.v1.views import app_views
from flask import abort
from flask import make_response


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def listall():
    amen = [obj.to_dict() for obj in storage.all(Amenity).values()]
    return jsonify(amen)


@app_views.route("/amenities/<string:amenity_id>", methods=["GET"],
                 strict_slashes=False)
def listone(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<string:amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delamen(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({})


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create():
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    amenity = request.get_json()
    new = Amenity(**amenity)
    new.save()
    return make_response(jsonify(new.to_dict()), 201)


@app_views.route("amenities/<string:amenity_id>", methods=['PUT'],
                 strict_slashes=False)
def update(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    requet = request.get_json()
    for key, value in requet.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict())
