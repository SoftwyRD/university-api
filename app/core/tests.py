from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.


def create_user(**params):
    user = get_user_model().objects.create(**params)
    return user


class UserModelTests(TestCase):
    def test_create_user_success(self):
        payload = {
            "first_name": "Test",
            "last_name": "User",
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpass123",
        }
        user = create_user(**payload)

        self.assertEqual(user.first_name, payload["first_name"])
        self.assertEqual(user.last_name, payload["last_name"])
        self.assertEqual(user.username, payload["username"])
        self.assertEqual(user.email, payload["email"])
        self.assertTrue(user.check_password(payload["password"]))

    def test_partial_update_user(self):
        payload = {
            "first_name": "Test",
            "last_name": "User",
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpass123",
        }
        new_username = "newtestuser"
        user = create_user(**payload)
        get_user_model().objects.update(username=new_username)
        user.refresh_from_db()

        self.assertEqual(user.first_name, payload["first_name"])
        self.assertEqual(user.last_name, payload["last_name"])
        self.assertEqual(user.username, new_username)
        self.assertEqual(user.email, payload["email"])
        self.assertTrue(user.check_password(payload["password"]))

    def test_delete_user(self):
        payload = {
            "first_name": "Test",
            "last_name": "User",
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpass123",
        }
        user = create_user(**payload)
        user.delete()
        user = get_user_model().objects.filter(username=payload["username"])

        self.assertFalse(user)

    def test_get_user(self):
        payload = {
            "first_name": "Test",
            "last_name": "User",
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpass123",
        }
        create_user(**payload)
        user = get_user_model().objects.get(username=payload["username"])

        self.assertTrue(user)

    def test_get_all_users(self):
        payload = {
            "first_name": "Test",
            "last_name": "User",
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpass123",
        }
        create_user(**payload)

        payload.update(
            {
                "first_name": "User",
                "last_name": "Test",
                "username": "usertest",
                "email": "usertest@example.com",
                "password": "passtest123",
            }
        )
        create_user(**payload)

        users = get_user_model().objects.all()

        self.assertEqual(users.count(), 2)
