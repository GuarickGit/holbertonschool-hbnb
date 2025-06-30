import unittest
from app.models.place import Place
from app.models.user import User

class TestPlaceModel(unittest.TestCase):

    def setUp(self):
        self.owner = User(first_name="Owner", last_name="User", email="owner@mail.com")

    def test_valid_place_creation(self):
        place = Place("Nice House", "Cozy place", 100.0, 45.0, 5.0, self.owner)
        self.assertEqual(place.title, "Nice House")
        self.assertEqual(place.price, 100.0)

    def test_invalid_empty_title(self):
        with self.assertRaises(ValueError):
            Place("", "desc", 50.0, 0.0, 0.0, self.owner)

    def test_invalid_negative_price(self):
        with self.assertRaises(ValueError):
            Place("Title", "desc", -20.0, 0.0, 0.0, self.owner)

    def test_invalid_latitude(self):
        with self.assertRaises(ValueError):
            Place("Title", "desc", 50.0, -100.0, 0.0, self.owner)

    def test_invalid_longitude(self):
        with self.assertRaises(ValueError):
            Place("Title", "desc", 50.0, 0.0, 200.0, self.owner)

    def test_update_valid_fields(self):
        place = Place("House", "desc", 100.0, 10.0, 20.0, self.owner)
        place.update({"title": "Villa", "price": 150.0})
        self.assertEqual(place.title, "Villa")
        self.assertEqual(place.price, 150.0)

    def test_update_invalid_title(self):
        place = Place("House", "desc", 100.0, 10.0, 20.0, self.owner)
        with self.assertRaises(ValueError):
            place.update({"title": ""})

    def test_update_invalid_price(self):
        place = Place("House", "desc", 100.0, 10.0, 20.0, self.owner)
        with self.assertRaises(ValueError):
            place.update({"price": -50})
