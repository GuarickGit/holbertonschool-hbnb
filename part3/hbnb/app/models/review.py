from app.models.base_model import BaseModel


class Review(BaseModel):
    """
    Represents a review of a place in the HBnB application.

    Inherits from BaseModel and includes review text, rating,
    and associations to a user and a place.
    """

    def __init__(self, text, rating, user, place):
        """
        Initialize a new Review instance with validation.

        Args:
            text (str): The content of the review. Must be a non-empty string.
            rating (int): An integer from 1 to 5 representing the review score.
            user (User): The user who wrote the review.
            place (Place): The place being reviewed.

        Raises:
            ValueError: If the text is invalid or the rating is out of range.
        """
        super().__init__()
        if not text or not isinstance(text, str):
            raise ValueError("Invalid review text")
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")
        self.text = text
        self.rating = rating
        self.user = user  # instance de User
        self.place = place  # instance de Place

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
