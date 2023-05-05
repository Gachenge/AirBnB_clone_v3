#!/usr/bin/python3
"""creating an API"""

from models import storage
from api.v1.views import app_views
from flask import Flask
from flask import jsonify
from flask import make_response
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)


@app.teardown_appcontext
def close(exception):
    storage.close()


@app.errorhandler(404)
def err404(exception):
    err = {"error": "Not found"}
    return make_response(jsonify(err), 404)


if __name__ == "__main__":
    import os

    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
