from app.models.base_model import BaseModel


class Amenity(BaseModel):
    """
    Represents an amenity in the HBnB application.
    Inherits from BaseModel and adds a validated 'name' attribute.
    """

    def __init__(self, name):
        """
        Initialize a new Amenity instance.

        Args:
            name (str): The name of the amenity. Must be a non-empty string with max length 50.

        Raises:
            ValueError: If the name is invalid.
        """
        super().__init__()

        if not isinstance(name, str) or not name or len(name) > 50:
            raise ValueError("Invalid amenity name")

        self.name = name

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
