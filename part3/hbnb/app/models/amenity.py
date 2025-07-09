from app.models.base_model import BaseModel
from app.extensions import db


class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)

    def update(self, data):
        """
        Update the amenity's name from a given data dictionary.

        Args:
            data (dict): Dictionary containing fields to update.

        Raises:
            ValueError: If the provided name is invalid.
        """
        if "name" in data:
            if not isinstance(data["name"], str) or not data["name"] or len(data["name"]) > 50:
                raise ValueError("Invalid name")
            self.name = data["name"]

        self.save()  # met à jour updated_at
