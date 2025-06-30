import uuid
from datetime import datetime


class BaseModel:
    """
    Base class that provides common attributes and behavior for all models.

    Attributes:
        id (str): A unique identifier for the instance (UUID).
        created_at (datetime): Timestamp when the instance was created.
        updated_at (datetime): Timestamp when the instance was last updated.
    """

    def __init__(self):
        """
        Initialize a new instance with a unique ID and timestamps.
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """
        Update the 'updated_at' timestamp to the current time.

        Should be called whenever the object is modified.
        """
        self.updated_at = datetime.now()

    def update(self, data):
        """
        Update the attributes of the object from a dictionary.

        Args:
            data (dict): Dictionary where keys are attribute names and values are new values.

        Notes:
            Only existing attributes will be updated. New attributes will be ignored.
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # Update the updated_at timestamp
