from app.models.base_model import BaseModel
from app.validators import is_valid_email
from app.extensions import db, bcrypt
import uuid
from .base_model import BaseModel  # Import BaseModel from its module


class User(BaseModel):
    """
    Represents a user of the application.

    Inherits:
        BaseModel: Provides ID, timestamps, and utility methods.

    Attributes:
        first_name (str): First name (required, max 50 characters).
        last_name (str): Last name (required, max 50 characters).
        email (str): Unique email address (required, max 120 characters).
        password (str): Hashed password (stored securely).
        is_admin (bool): Indicates if the user has admin privileges.
        places (List[Place]): Places owned by the user.
        reviews (List[Review]): Reviews authored by the user.
    """

    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    places = db.relationship('Place', backref='owner', lazy=True)
    reviews = db.relationship('Review', back_populates='user', lazy=True)


    def update(self, data):
        """
        Update the user's information.

        Args:
            data (dict): May include "first_name", "last_name", or "email".

        Raises:
            ValueError: If any field is invalid (wrong type, format, or length).
        """
        if "first_name" in data:
            if not isinstance(data["first_name"], str) or not data["first_name"] or len(data["first_name"]) > 50:
                raise ValueError("Invalid first_name")
            self.first_name = data["first_name"]

        if "last_name" in data:
            if not isinstance(data["last_name"], str) or not data["last_name"] or len(data["last_name"]) > 50:
                raise ValueError("Invalid last_name")
            self.last_name = data["last_name"]

        if "email" in data:
            if not isinstance(data["email"], str) or not data["email"] or not is_valid_email(data["email"]):
                raise ValueError("Invalid email")
            self.email = data["email"]

        self.save()  # met à jour updated_at

    def hash_password(self, password):
        """
        Hash and store the given password securely.

        Args:
            password (str): Plain-text password to hash.
        """
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """
        Check if the provided password matches the stored hash.

        Args:
            password (str): Plain-text password to verify.

        Returns:
            bool: True if password is correct, False otherwise.
        """
        return bcrypt.check_password_hash(self.password, password)
