from app.models.base_model import BaseModel
from app.validators import is_valid_email
from app.extensions import db, bcrypt
import uuid
from .base_model import BaseModel  # Import BaseModel from its module


class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def update(self, data):
        """
        Update the user's attributes using a dictionary of new values.

        Args:
            data (dict): Dictionary with optional 'first_name', 'last_name', or 'email' keys.

        Raises:
            ValueError: If any provided field is invalid.
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
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)
