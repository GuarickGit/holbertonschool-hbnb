from app.models.base_model import BaseModel
from app.extensions import db


class Amenity(BaseModel):
    """
    Represents an amenity that can be associated with places (e.g., Wi-Fi, Pool, Parking).

    Inherits from:
        BaseModel: Provides ID, created_at, updated_at fields and utility methods.

    Attributes:
        name (str): Name of the amenity. Must be a non-empty string of max 50 characters.
    """

    __tablename__ = 'amenities'

    name = db.Column(db.String(255), nullable=False, unique=True)

    def update(self, data):
        """
        Update the amenity's name from a given data dictionary.

        Args:
            data (dict): Dictionary containing fields to update. Supported key: "name".

        Raises:
            ValueError: If the provided name is not a valid non-empty string ≤ 50 characters.
        """
        if "name" in data:
            new_name = data["name"]
            if not isinstance(new_name, str) or not new_name or len(new_name) > 255:
                raise ValueError("Invalid name")

            # Vérifie qu'aucune autre amenity n'a ce nom
            existing = Amenity.query.filter(
                Amenity.name == new_name,
                Amenity.id != self.id
            ).first()
            if existing:
                raise ValueError("Amenity name already exists")

            self.name = new_name

        self.save()
