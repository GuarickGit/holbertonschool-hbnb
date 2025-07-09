from app.models.base_model import BaseModel
from app.extensions import db

class Review(BaseModel):
    __tablename__= 'reviews'
    text = db.Column(db.String(1000), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    def update(self, review_data):
        """
        Update the review with new values from a dictionary.

        Args:
            review_data (dict): Dictionary with optional 'text' and 'rating' keys.

        Raises:
            ValueError: If the provided values are invalid.
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
