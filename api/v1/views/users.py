#!/usr/bin/python3

"""view for user handles all default RESTFul API actions"""

from api.v1.views import app_views
from models import storage
from models.user import User
from flask import jsonify
from flask import request
from flask import abort
from flask import make_response


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def listusers():
    users = [obj.to_dict() for obj in storage.all(User).values()]
    return jsonify(users)


@app_views.route("/users/<string:user_id>", methods=["GET"],
                 strict_slashes=False)
def oneuser(user_id):
    users = storage.get(User, user_id)
    if users is None:
        abort(404)
    return jsonify(users.to_dict())


@app_views.route("/users/<string:user_id>", methods=["DELETE"],
                 strict_slashes=False)
def deluser(user_id):
    users = storage.get(User, user_id)
    if users is None:
        abort(404)
    users.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def creuser():
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'email' not in request.get_json():
        return make_response(jsonify({"error": "Missing email"}), 400)
    if 'password' not in request.get_json():
        return make_response(jsonify({"error": "Missing password"}), 400)
    requet = request.get_json()
    new = User(**requet)
    new.save()
    return jsonify(new.to_dict()), 201


@app_views.route("/users/<string:user_id>", methods=["PUT"],
                 strict_slashes=False)
def updat(user_id):
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict())
