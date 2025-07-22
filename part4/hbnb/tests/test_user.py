import unittest
from app.models.user import User
import datetime

class TestUserModel(unittest.TestCase):

    def test_valid_user_creation(self):
        user = User(first_name="Alice", last_name="Smith", email="alice@mail.com")
        self.assertEqual(user.first_name, "Alice")
        self.assertEqual(user.last_name, "Smith")
        self.assertEqual(user.email, "alice@mail.com")

    def test_invalid_empty_first_name(self):
        with self.assertRaises(ValueError):
            User(first_name="", last_name="Smith", email="alice@mail.com")

    def test_invalid_empty_last_name(self):
        with self.assertRaises(ValueError):
            User(first_name="Alice", last_name="", email="alice@mail.com")

    def test_invalid_email_format(self):
        with self.assertRaises(ValueError):
            User(first_name="Alice", last_name="Smith", email="invalid-email")

    def test_update_valid_fields(self):
        user = User(first_name="Alice", last_name="Smith", email="alice@mail.com")
        user.update({
            "first_name": "Bob",
            "last_name": "Brown",
            "email": "bob@mail.com"
        })
        self.assertEqual(user.first_name, "Bob")
        self.assertEqual(user.last_name, "Brown")
        self.assertEqual(user.email, "bob@mail.com")

    def test_update_invalid_first_name(self):
        user = User(first_name="Alice", last_name="Smith", email="alice@mail.com")
        with self.assertRaises(ValueError):
            user.update({"first_name": ""})

    def test_update_invalid_last_name(self):
        user = User(first_name="Alice", last_name="Smith", email="alice@mail.com")
        with self.assertRaises(ValueError):
            user.update({"last_name": ""})

    def test_update_invalid_email(self):
        user = User(first_name="Alice", last_name="Smith", email="alice@mail.com")
        with self.assertRaises(ValueError):
            user.update({"email": "bad-email"})

    def test_inherited_fields_exist(self):
        user = User(first_name="Alice", last_name="Smith", email="alice@mail.com")
        self.assertTrue(hasattr(user, 'id'))
        self.assertTrue(hasattr(user, 'created_at'))
        self.assertTrue(hasattr(user, 'updated_at'))
        self.assertIsInstance(user.created_at, datetime.datetime)
        self.assertIsInstance(user.updated_at, datetime.datetime)

    def test_default_is_admin_false(self):
        user = User(first_name="Alice", last_name="Smith", email="alice@mail.com")
        self.assertFalse(user.is_admin)

    def test_custom_is_admin_true(self):
        user = User(first_name="Admin", last_name="Root", email="admin@mail.com", is_admin=True)
        self.assertTrue(user.is_admin)

if __name__ == '__main__':
    unittest.main()
