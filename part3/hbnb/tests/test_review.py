import unittest
from app.models.review import Review
from app.models.user import User
from app.models.place import Place

class TestReviewModel(unittest.TestCase):

    def setUp(self):
        self.user = User("John", "Doe", "john@mail.com")
        self.place = Place("Flat", "desc", 100.0, 45.0, 45.0, self.user)

    def test_valid_review_creation(self):
        review = Review("Nice place", 5, self.user, self.place)
        self.assertEqual(review.text, "Nice place")
        self.assertEqual(review.rating, 5)

    def test_invalid_empty_text(self):
        with self.assertRaises(ValueError):
            Review("", 4, self.user, self.place)

    def test_invalid_rating_type(self):
        with self.assertRaises(ValueError):
            Review("Text", "bad", self.user, self.place)

    def test_invalid_rating_range(self):
        with self.assertRaises(ValueError):
            Review("Text", 10, self.user, self.place)

    def test_update_valid_review(self):
        review = Review("Nice", 5, self.user, self.place)
        review.update({"text": "Updated", "rating": 4})
        self.assertEqual(review.text, "Updated")
        self.assertEqual(review.rating, 4)

    def test_update_invalid_text(self):
        review = Review("Nice", 5, self.user, self.place)
        with self.assertRaises(ValueError):
            review.update({"text": ""})

    def test_update_invalid_rating(self):
        review = Review("Nice", 5, self.user, self.place)
        with self.assertRaises(ValueError):
            review.update({"rating": 8})
