from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.

PAYLOAD = {
    "first_name": "Test",
    "last_name": "User",
    "username": "testuser",
    "email": "testuser@example.com",
    "password": "testpass123",
}


def create_user(**params):
    user = get_user_model().objects.create(**params)
    return user


class UserModelTests(TestCase):
    def test_create_user_success(self):
        user = create_user(**PAYLOAD)

        self.assertEqual(user.first_name, PAYLOAD["first_name"])
        self.assertEqual(user.last_name, PAYLOAD["last_name"])
        self.assertEqual(user.username, PAYLOAD["username"])
        self.assertEqual(user.email, PAYLOAD["email"])
        self.assertTrue(user.check_password(PAYLOAD["password"]))

    def test_partial_update_user(self):
        new_username = "newtestuser"
        user = create_user(**PAYLOAD)
        get_user_model().objects.update(username=new_username)
        user.refresh_from_db()

        self.assertEqual(user.first_name, PAYLOAD["first_name"])
        self.assertEqual(user.last_name, PAYLOAD["last_name"])
        self.assertEqual(user.username, new_username)
        self.assertEqual(user.email, PAYLOAD["email"])
        self.assertTrue(user.check_password(PAYLOAD["password"]))

    def test_delete_user(self):
        user = create_user(**PAYLOAD)
        user.delete()
        user = get_user_model().objects.filter(username=PAYLOAD["username"])

        self.assertFalse(user)

    def test_get_user(self):
        create_user(**PAYLOAD)
        user = get_user_model().objects.get(username=PAYLOAD["username"])

        self.assertTrue(user)

    def test_get_all_users(self):
        create_user(**PAYLOAD)

        PAYLOAD.update(
            {
                "first_name": "User",
                "last_name": "Test",
                "username": "usertest",
                "email": "usertest@example.com",
                "password": "passtest123",
            }
        )
        create_user(**PAYLOAD)

        users = get_user_model().objects.all()

        self.assertEqual(users.count(), 2)
