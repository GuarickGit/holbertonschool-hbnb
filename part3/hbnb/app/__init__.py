from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns
from app.api.v1.admins import api as admins_ns

from werkzeug.utils import import_string
from app.extensions import bcrypt
from flask_jwt_extended import JWTManager

jwt = JWTManager()

def create_app(config_class="config.DevelopmentConfig"):
    """
    Creates and configures the Flask application instance with Flask-RESTX.

    Registers all API namespaces under the `/api/v1` path.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(import_string(config_class))

    authorizations = {
    'Bearer': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'JWT Authorization header using the Bearer scheme. Example: "Bearer {token}"'
    }
}

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
