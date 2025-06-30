from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class HBnBFacade:
    """
    Facade class that provides a simplified interface to interact with
    users, amenities, places, and reviews using in-memory repositories.
    """

    def __init__(self):
        """
        Initializes repositories for users, places, reviews, and amenities.
        """
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # -------------------------------
    # User Methods
    # -------------------------------

    def create_user(self, user_data):
        """
        Creates a new user and stores it in the repository.

        Args:
            user_data (dict): Dictionary containing user attributes.

        Returns:
            User: The created user object.
        """
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """
        Retrieves a user by ID.

        Args:
            user_id (str): ID of the user.

        Returns:
            User or None: The user object if found, otherwise None.
        """
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """
        Retrieves a user by email address.

        Args:
            email (str): The user's email.

        Returns:
            User or None: The user object if found, otherwise None.
        """
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        """
        Retrieves all users.

        Returns:
            list[User]: A list of all user objects.
        """
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """
        Updates user data by ID.

        Args:
            user_id (str): ID of the user.
            user_data (dict): Data to update.

        Returns:
            User or None: The updated user object, or None if not found.
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
        """
        Creates a new amenity.

        Args:
            amenity_data (dict): Data for the new amenity.

        Returns:
            Amenity: The created amenity object.
        """
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """
        Retrieves an amenity by ID.

        Args:
            amenity_id (str): ID of the amenity.

        Returns:
            Amenity or None
        """
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """
        Retrieves all amenities.

        Returns:
            list[Amenity]: List of all amenity objects.
        """
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """
        Updates an amenity by ID.

        Args:
            amenity_id (str): ID of the amenity.
            amenity_data (dict): Data to update.

        Returns:
            Amenity or None: Updated amenity object or None if not found.
        """
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
        Creates a new place with linked owner and amenities.

        Args:
            place_data (dict): Data for the new place.

        Returns:
            Place: The created place object.

        Raises:
            ValueError: If owner or any amenity is not found.
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
        """
        Retrieves a place by ID.

        Args:
            place_id (str): ID of the place.

        Returns:
            Place or None
        """
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """
        Retrieves all places.

        Returns:
            list[Place]: List of all place objects.
        """
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """
        Updates an existing place.

        Args:
            place_id (str): ID of the place to update.
            place_data (dict): Fields to update.

        Returns:
            Place or None: Updated place or None if not found.

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
        Creates a new review associated with a user and a place.

        Args:
            review_data (dict): Data for the review.

        Returns:
            Review: The created review object.

        Raises:
            ValueError: If user/place is not found or data is invalid.
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
        """
        Retrieves a review by ID.

        Args:
            review_id (str): ID of the review.

        Returns:
            Review or None
        """
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """
        Retrieves all reviews.

        Returns:
            list[Review]: All review objects.
        """
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """
        Retrieves all reviews for a specific place.

        Args:
            place_id (str): ID of the place.

        Returns:
            list[Review]: Reviews linked to the specified place.
        """
        return [review for review in self.review_repo.get_all() if review.place.id == place_id]

    def update_review(self, review_id, review_data):
        """
        Updates a review's content and rating.

        Args:
            review_id (str): ID of the review.
            review_data (dict): Fields to update.

        Returns:
            Review or None
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
        Deletes a review and removes it from the associated place.

        Args:
            review_id (str): ID of the review.

        Returns:
            bool: True if deletion was successful, False otherwise.
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
