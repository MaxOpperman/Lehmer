# filepath: c:\Users\Max\Documents\GitHub\Lehmer\app\__init__.py
from flask import Flask, app
from flask_cors import CORS

from app.routes import routes


def create_app(allow_cors=False):
    app = Flask(__name__)
    if allow_cors:
        CORS(app)
    # Register blueprints
    app.register_blueprint(routes)

    return app
