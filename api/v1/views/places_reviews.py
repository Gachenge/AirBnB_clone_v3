#!/usr/bin/python3

"""view for review object handles all default RESTFul API"""

from models import storage
from api.v1.views import app_views
from models.review import Review
from models.place import Place
from flask import abort
from flask import jsonify
from flask import request
from models.user import User
from flask import make_response


@app_views.route("/places/<place_id>/reviews", methods=['GET'],
                 strict_slashes=False)
def listrev(place_id):
    places = storage.get(Place, place_id)
    if places is None:
        abort(404)
    review = [obj.to_dict() for obj in places.reviews]
    return jsonify(review)


@app_views.route("/reviews/<review_id>", methods=["GET"],
                 strict_slashes=False)
def onerev(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def deleview(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({})


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def creareview(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'user_id' not in request.get_json():
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    requet = request.get_json()
    user = storage.get(User, requet['user_id'])
    if user is None:
        abort(404)
    if 'text' not in request.get_json():
        return make_response(jsonify({"error": "Missing text"}), 400)
    requet['place_id'] = place_id
    new = Review(**requet)
    new.save()
    return make_response(jsonify(new.to_dict()), 201)


@app_views.route("/reviews/<review_id>", methods=["PUT"],
                 strict_slashes=False)
def updareview(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in request.get_json().items():
        if key not in ['id', 'user_id', 'place_id', 'created_at'
                       'updated_at']:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict())
