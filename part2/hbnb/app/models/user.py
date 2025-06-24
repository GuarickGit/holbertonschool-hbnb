from app.models.base_model import BaseModel
from app.validators import is_valid_email


class User(BaseModel):
    """
    Represents a user in the HBnB application.

    Inherits from BaseModel and includes basic user attributes
    such as first name, last name, email, and admin status.
    """

    def __init__(self, first_name, last_name, email, is_admin=False):
        """
        Initialize a new User instance with validation.

        Args:
            first_name (str): User's first name (max 50 characters).
            last_name (str): User's last name (max 50 characters).
            email (str): User's email address. Must be valid.
            is_admin (bool, optional): Whether the user has admin rights. Defaults to False.

        Raises:
            ValueError: If any input is invalid.
        """
        super().__init__()

        if not isinstance(first_name, str) or not first_name or len(first_name) > 50:
            raise ValueError("Invalid first_name")
        if not isinstance(last_name, str) or not last_name or len(last_name) > 50:
            raise ValueError("Invalid last_name")
        if not isinstance(email, str) or not email or not is_valid_email(email):
            raise ValueError("Invalid email")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

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
