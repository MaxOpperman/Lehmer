# filepath: c:\Users\Max\Documents\GitHub\Lehmer\app\__init__.py
from flask import Flask
from flask_cors import CORS

from app.routes import routes


def create_app(allow_cors: bool = False) -> Flask:
    """
    Creates the flask app

    Args:
        allow_cors (bool, optional): Whether to allow CORS for the app. Defaults to False.

    Returns:
        Flask: The created Flask app.
    """
    app = Flask(__name__)
    if allow_cors:
        CORS(app)
    # Register blueprints
    app.register_blueprint(routes)

    return app
