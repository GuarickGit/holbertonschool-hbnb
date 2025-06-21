import unittest
from app.models.amenity import Amenity

class TestAmenityModel(unittest.TestCase):

    def test_valid_amenity_creation(self):
        amenity = Amenity("WiFi")
        self.assertEqual(amenity.name, "WiFi")

    def test_invalid_empty_name(self):
        with self.assertRaises(ValueError):
            Amenity("")

    def test_invalid_name_type(self):
        with self.assertRaises(ValueError):
            Amenity(123)

    def test_invalid_name_length(self):
        long_name = "A" * 100
        with self.assertRaises(ValueError):
            Amenity(long_name)

    def test_update_valid_name(self):
        amenity = Amenity("WiFi")
        amenity.update({"name": "Pool"})
        self.assertEqual(amenity.name, "Pool")

    def test_update_invalid_name(self):
        amenity = Amenity("WiFi")
        with self.assertRaises(ValueError):
            amenity.update({"name": ""})
