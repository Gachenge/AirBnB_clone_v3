#!/usr/bin/python3

"""a view for state objects to handle all default restful API actions"""

from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify
from flask import abort
from flask import request
from flask import make_response


@app_views.route("/states", methods=["GET"],
                 strict_slashes=False)
def states():
    """view for state objects"""
    objects = [obj.to_dict() for obj in storage.all(State).values()]
    return jsonify(objects)


@app_views.route("/states/<string:state_id>", methods=["GET"],
                 strict_slashes=False)
def statid(state_id):
    """view for state matched with id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<string:state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delid(state_id):
    """deletes a state object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", methods=["POST"],
                 strict_slashes=False)
def addst():
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    state = request.get_json()
    new = State(**state)
    new.save()
    return jsonify(new.to_dict()), 201


@app_views.route("/states/<string:state_id>", methods=["PUT"],
                 strict_slashes=False)
def updst(state_id):
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    states = request.get_json()
    for key, value in states.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    return (jsonify(state.to_dict()), 200)
