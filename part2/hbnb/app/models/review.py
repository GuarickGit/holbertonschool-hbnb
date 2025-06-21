from app.models.base_model import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, user, place):
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
        if "text" in review_data:
            if not review_data["text"] or not isinstance(review_data["text"], str):
                raise ValueError("Invalid review text")
            self.text = review_data["text"]

        if "rating" in review_data:
            if not isinstance(review_data["rating"], int) or not (1 <= review_data["rating"] <= 5):
                raise ValueError("Invalid rating")
            self.rating = review_data["rating"]

        self.save()
