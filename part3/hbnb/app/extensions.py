"""
Initialize shared Flask extensions.

These extensions are imported in the app factory and used across the application.
"""

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy instance used for ORM
db = SQLAlchemy()
# Bcrypt instance used for password hashing
bcrypt = Bcrypt()
