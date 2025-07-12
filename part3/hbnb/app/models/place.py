from app.models.base_model import BaseModel
from app.extensions import db
import uuid
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

# Association table for many-to-many relationship between Place and Amenity
place_amenities = db.Table('place_amenities',
        db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
        db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
    )

class Place(BaseModel):
    """
    Represents a place available for booking.

    Inherits:
        BaseModel: Includes ID, timestamps, and persistence methods.

    Attributes:
        title (str): Title of the place (max 100 chars).
        description (str): Description of the place (optional, max 3000 chars).
        price (float): Price per night (must be > 0).
        latitude (float): Geographical latitude (-90 to 90).
        longitude (float): Geographical longitude (-180 to 180).
        user_id (int): Foreign key to the owner (User).
        reviews (List[Review]): Linked reviews.
        amenities (List[Amenity]): Linked amenities through many-to-many.
    """

    __tablename__ = 'places'

    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(3000), nullable=False)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    reviews = db.relationship('Review', backref='place', lazy=True)
    amenities = db.relationship('Amenity', secondary=place_amenities, backref=db.backref('places', lazy=True))
    reviews = db.relationship('Review', back_populates='place', lazy=True)


    def add_review(self, review):
        """
        Link a Review to this Place.

        Args:
            review (Review): Review instance to associate.
        """
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """
        Link an Amenity to this Place.

        Args:
            amenity (Amenity): Amenity instance to associate.
        """
        self.amenities.append(amenity)

    def update(self, place_data):
        """
        Update the Place using provided values.

        Args:
            place_data (dict): Dictionary of attributes to update.

        Raises:
            ValueError: If any provided field is invalid or outside acceptable bounds.
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
