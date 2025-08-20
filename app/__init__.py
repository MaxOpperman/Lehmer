# filepath: c:\Users\Max\Documents\GitHub\Lehmer\app\__init__.py
from flask import Flask
from flask_cors import CORS

from app.routes import routes


def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes

    # Register blueprints
    app.register_blueprint(routes)

    return app
