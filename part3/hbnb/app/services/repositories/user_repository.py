from app.models.user import User
from app.extensions import db
from app.persistence.repository import SQLAlchemyRepository

class UserRepository(SQLAlchemyRepository):
    """
    Repository class for managing User entities in the database.

    Inherits:
        SQLAlchemyRepository: Provides basic CRUD operations.

    Methods:
        get_user_by_email(email): Retrieve a user by their email address.
    """
    def __init__(self):
        """
        Initialize the UserRepository with the User model.
        """
        super().__init__(User)

    def get_user_by_email(self, email):
        """
        Retrieve a user based on their email.

        Args:
            email (str): The email address to search for.

        Returns:
            User: The user instance if found, otherwise None.
        """
        return self.model.query.filter_by(email=email).first()
