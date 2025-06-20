from app.models.base_model import BaseModel

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()

        if not title or len(title) > 100:
            raise ValueError("Invalid title")
        if price <= 0:
            raise ValueError("Price must be positive")
        if not (-90 <= latitude <= 90):
            raise ValueError("Latitude out of range")
        if not (-180 <= longitude <= 180):
            raise ValueError("Longitude out of range")

        self.title = title
        self.description = description or ""
        self.price = float(price)
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner  # instance de User
        self.reviews = []
        self.amenities = []

    def add_review(self, review):
        self.reviews.append(review)

    def add_amenity(self, amenity):
        self.amenities.append(amenity)
