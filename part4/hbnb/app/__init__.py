"""
Initialize and configure the HBnB Flask application.

This module creates the Flask app instance, sets up extensions (SQLAlchemy, Bcrypt, JWT),
and registers all API namespaces under the `/api/v1` prefix.

Modules registered:
- Users
- Amenities
- Places
- Reviews
- Auth
- Admins
"""

from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns
from app.api.v1.admins import api as admins_ns

from werkzeug.utils import import_string
from app.extensions import db, bcrypt
from flask_jwt_extended import JWTManager

from flask_cors import CORS

jwt = JWTManager()

def create_app(config_class="config.DevelopmentConfig"):
    """
    Create and configure the Flask application instance.

    Sets up:
    - Flask-RESTX for API management
    - SQLAlchemy for ORM
    - Bcrypt for password hashing
    - JWTManager for authentication
    - All registered API namespaces under /api/v1

    Args:
        config_class (str): Python path to the configuration class to load.

    Returns:
        Flask: The configured Flask application.
    """
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "http://localhost:8000"}}, supports_credentials=True)
    app.config.from_object(import_string(config_class))
    db.init_app(app)

    authorizations = {
    'Bearer': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'JWT Authorization header using the Bearer scheme. Example: "Bearer {token}"'
    }
}
     # Initialize RESTX API with metadata
    api = Api(app,
            version='1.0',
            title='HBnB API',
            description='HBnB Application API',
            authorizations=authorizations,
            security='Bearer')

    bcrypt.init_app(app)
    jwt.init_app(app)

    # Register the users namespace
    api.add_namespace(users_ns, path='/api/v1/users')
    # Register the amenities namespace
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    # Register the places namespace
    api.add_namespace(places_ns, path='/api/v1/places')
    # Register the reviews namespace
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    # Register the auth namespace
    api.add_namespace(auth_ns, path='/api/v1/auth')
    # Register the admin namespace
    api.add_namespace(admins_ns, path='/api/v1/admins')

    return app
