from app.models.base_model import BaseModel
from app.extensions import db
import uuid


class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(3000), nullable=False)
    price = db.Column(db.Float(20), nullable=False)
    latitude = db.Column(db.Float(50), nullable=False)
    longitude = db.Column(db.Float(50), nullable=False)

    def add_review(self, review):
        """
        Add a review to the place.

        Args:
            review (Review): The review to add.
        """
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """
        Add an amenity to the place.

        Args:
            amenity (Amenity): The amenity to add.
        """
        self.amenities.append(amenity)

    def update(self, place_data):
        """
        Update the place's attributes using a dictionary of new values.

        Args:
            place_data (dict): Dictionary of attributes to update.

        Raises:
            ValueError: If any provided field is invalid.
        """

        if "title" in place_data:
            if not isinstance(place_data["title"], str) or not place_data["title"] or len(place_data["title"]) > 100:
                raise ValueError("Invalid title")
            self.title = place_data["title"]

        if "description" in place_data:
            if place_data["description"] is not None and not isinstance(place_data["description"], str):
                raise ValueError("Invalid description")
            self.description = place_data["description"] or ""

        if "price" in place_data:
            if not isinstance(place_data["price"], (int, float)) or place_data["price"] <= 0:
                raise ValueError("Invalid price")
            self.price = place_data["price"]

        if "latitude" in place_data:
            if not isinstance(place_data["latitude"], (int, float)) or not (-90 <= place_data["latitude"] <= 90):
                raise ValueError("Invalid latitude")
            self.latitude = place_data["latitude"]

        if "longitude" in place_data:
            if not isinstance(place_data["longitude"], (int, float)) or not (-180 <= place_data["longitude"] <= 180):
                raise ValueError("Invalid longitude")
            self.longitude = place_data["longitude"]

        self.save()
