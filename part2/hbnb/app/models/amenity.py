from app.models.base_model import BaseModel


class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()

        if not isinstance(name,str) or not name or len(name) > 50:
            raise ValueError("Invalid amenity name")

        self.name = name

    def update(self, data):
        if "name" in data:
            if not isinstance(data["name"], str) or not data["name"] or len(data["name"]) > 50:
                raise ValueError("Invalid name")
            self.name = data["name"]

        self.save()  # met à jour updated_at
