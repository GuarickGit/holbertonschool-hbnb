from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # User Methods

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        user = self.get_user(user_id)
        if not user:
            return None
        user.update(user_data)
        return user

    # Amenity Methods

    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None
        amenity.update(amenity_data)
        return amenity

    # Place Methods

    def create_place(self, place_data):
        # 1. Extraire les IDs
        owner_id = place_data.get("owner_id")
        amenity_ids = place_data.get("amenities", [])

        # 2. Vérifier que l'owner existe
        owner = self.user_repo.get(owner_id)
        if not owner:
            raise ValueError("Owner not found")

        # 3. Récupérer les objets amenity (et valider)
        amenities = []
        for amenity_id in amenity_ids:
            amenity = self.amenity_repo.get(amenity_id)
            if not amenity:
                raise ValueError(f"Amenity not found: {amenity_id}")
            amenities.append(amenity)

        # 4. Nettoyer les données à passer à Place (on retire owner_id et amenities)
        place_fields = place_data.copy()
        place_fields.pop("owner_id", None)
        place_fields.pop("amenities", None)

        # 5. Créer la place avec les bons arguments
        place = Place(**place_fields, owner=owner)

        # 6. Ajouter les amenities à l'objet
        for amenity in amenities:
            place.add_amenity(amenity)

        # 7. Enregistrer
        self.place_repo.add(place)

        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)
        if not place:
            return None

        # Ne surtout pas écraser owner
        if "owner_id" in place_data:
            place_data.pop("owner_id")

        # Si des amenities sont fournies : les mettre à jour aussi
        if "amenities" in place_data:
            new_amenity_ids = place_data.pop("amenities")
            new_amenities = []
            for amenity_id in new_amenity_ids:
                amenity = self.get_amenity(amenity_id)
                if not amenity:
                    raise ValueError(f"Amenity not found: {amenity_id}")
                new_amenities.append(amenity)
            place.amenities = new_amenities

        # Mise à jour des autres champs
        place.update_place(place_data)

        return place
