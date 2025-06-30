from app.models.base_model import BaseModel


class Place(BaseModel):
    """
    Represents a place listing in the HBnB application.

    Inherits from BaseModel and includes details like title, price, location,
    owner, amenities, and reviews.
    """

    def __init__(self, title, description, price, latitude, longitude, owner):
        """
        Initialize a new Place instance with validated attributes.

        Args:
            title (str): Title of the place (max 100 characters).
            description (str): Optional description of the place.
            price (float): Price of the place. Must be > 0.
            latitude (float): Latitude (-90 to 90).
            longitude (float): Longitude (-180 to 180).
            owner (User): The user who owns the place.

        Raises:
            ValueError: If any of the parameters are invalid.
        """
        super().__init__()

        if not isinstance(title, str) or not title or len(title) > 100:
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
