from app.persistence.repository import SQLAlchemyRepository
from app.services.repositories.user_repository import UserRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class HBnBFacade:
    """
    Facade service layer that centralizes business logic and coordinates
    interactions between repositories and models.

    Provides a simplified and consistent interface for:
        - User management
        - Place creation and updating
        - Amenity management
        - Review handling
    """

    def __init__(self):
        """
        Initialize repositories for each model.
        """
        self.user_repo = UserRepository()
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)

    # -------------------------------
    # User Methods
    # -------------------------------

    def create_user(self, user_data):
        """
        Create and persist a new user after hashing the password.

        Args:
            user_data (dict): New user data.

        Returns:
            User: The created user instance.
        """
        user = User(**user_data)
        user.hash_password(user_data['password'])
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Retrieve a user by ID."""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Retrieve a user by their email."""
        return self.user_repo.get_user_by_email(email)

    def get_all_users(self):
        """Return all registered users."""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """
        Update user attributes.

        Args:
            user_id (str): Target user ID.
            user_data (dict): Fields to update.

        Returns:
            User or None: Updated user or None if not found.
        """
        user = self.get_user(user_id)
        if not user:
            return None
        user.update(user_data)
        return user

    # -------------------------------
    # Amenity Methods
    # -------------------------------

    def create_amenity(self, amenity_data):
        """Create and save a new amenity."""
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Retrieve an amenity by ID."""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Return all amenities."""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update an amenity's data by ID."""
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None
        amenity.update(amenity_data)
        return amenity

    # -------------------------------
    # Place Methods
    # -------------------------------

    def create_place(self, place_data):
        """
        Create a new place associated with an owner and optional amenities.

        Raises:
            ValueError: If owner or an amenity is not found.
        """
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
        """Retrieve a place by ID."""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Return all places."""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """
        Update place attributes and amenities.

        Raises:
            ValueError: If any new amenity is not found.
        """
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
        place.update(place_data)

        return place

    # -------------------------------
    # Review Methods
    # -------------------------------

    def create_review(self, review_data):
        """
        Create a review for a given place and user.

        Raises:
            ValueError: If user/place not found or data invalid.
        """
        # 1. Extraire les IDs
        user_id = review_data.get("user_id")
        place_id = review_data.get("place_id")
        rating = review_data.get("rating")

        # 2. Vérifier que l'owner existe
        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError("User not found")

        # 3. Vérifier que la place existe
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")

        # 4. Vérifier que le rating existe
        if rating is None or not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")

        # 5. Récupérer le texte
        text = review_data.get("text")
        if not text or not isinstance(text, str):
            raise ValueError("Invalid review text")

        # 6. Créer le Review
        review = Review(text=text, rating=rating, user=user, place=place)

        # 7. Ajouter à la place
        place.reviews.append(review)

        # 8. Ajouter au repo
        self.review_repo.add(review)

        # 9. Retourner
        return review

    def get_review(self, review_id):
        """Retrieve a review by ID."""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Return all reviews."""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """Return all reviews for a given place ID."""
        return [review for review in self.review_repo.get_all() if review.place.id == place_id]

    def update_review(self, review_id, review_data):
        """
        Update a review's content and rating.

        Ignores changes to user_id and place_id.
        """
        review = self.get_review(review_id)
        if not review:
            return None

        # Ne pas permettre de changer user ou place
        review_data.pop("user_id", None)
        review_data.pop("place_id", None)

        # Mise à jour des champs valides
        review.update(review_data)
        return review

    def delete_review(self, review_id):
        """
        Delete a review and remove it from its associated place.

        Returns:
            bool: True if successful, False if review not found.
        """
        review = self.get_review(review_id)
        if not review:
            return False

        # Retirer la review du repo
        self.review_repo.delete(review_id)

        # Retirer aussi la review de la place correspondante
        if review.place and review in review.place.reviews:
            review.place.reviews.remove(review)

        return True
