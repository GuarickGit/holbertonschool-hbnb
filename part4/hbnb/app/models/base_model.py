from app.extensions import db
import uuid
from datetime import datetime


class BaseModel(db.Model):
    """
    Abstract base model providing common fields and methods for all models.

    Fields:
        id (str): Unique identifier (UUIDv4).
        created_at (datetime): Timestamp when the object was created.
        updated_at (datetime): Timestamp when the object was last updated.

    Methods:
        save(): Persist the current state of the object to the database.
        update(data: dict): Update object's attributes with the given data.
    """

    __abstract__ = True  # This ensures SQLAlchemy does not create a table for BaseModel

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def save(self):
        """
        Persist the object in the database and refresh the 'updated_at' field.

        Commits the current session after saving.
        """
        self.updated_at = datetime.now()
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        """
        Update object fields based on the provided dictionary.

        Args:
            data (dict): A dictionary with keys matching attribute names to update.

        Notes:
            - Only attributes that already exist will be updated.
            - Fields not defined on the model will be ignored.
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # Update the updated_at timestamp
