from app.models.base_model import BaseModel
from app.extensions import db

class Review(BaseModel):
    """
    Represents a user's review for a place.

    Inherits:
        BaseModel: Provides ID, timestamps, and utility methods.

    Attributes:
        text (str): The content of the review (max 1000 characters, required).
        rating (int): Rating between 1 and 5.
        place_id (int): Foreign key linking to the reviewed Place.
        user_id (int): Foreign key linking to the reviewing User.
    """

    __tablename__= 'reviews'
    text = db.Column(db.String(1000), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    place_id = db.Column(db.Integer, db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def update(self, review_data):
        """
        Update the review's content and/or rating.

        Args:
            review_data (dict): Keys may include "text" and/or "rating".

        Raises:
            ValueError: If any provided field is invalid:
                - text must be a non-empty string.
                - rating must be an integer between 1 and 5.
        """
        if "text" in review_data:
            if not review_data["text"] or not isinstance(review_data["text"], str):
                raise ValueError("Invalid review text")
            self.text = review_data["text"]

        if "rating" in review_data:
            if not isinstance(review_data["rating"], int) or not (1 <= review_data["rating"] <= 5):
                raise ValueError("Invalid rating")
            self.rating = review_data["rating"]

        self.save()
