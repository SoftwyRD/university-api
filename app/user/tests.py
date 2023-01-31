from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

# Create your tests here.

USER_URL = reverse("user")
LOGIN_URL = reverse("user:login")


class UserPublicApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_register_user_success(self):
        PAYLOAD = {
            "first_name": "Test",
            "last_name": "User",
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpass123",
        }

        res = self.client.post(USER_URL, PAYLOAD)
        res_status = res.data["status"]
        res_data = res.data["data"]
        user = res_data["user"]
        user_location = f"/api/users/{user.id}/"

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res["Location"], user_location)
        self.assertEqual(res_status, "success")
        self.assertEqual(user["username"], PAYLOAD["username"])
        self.assertNotIn("password", user)

    def test_login_not_registered(self):
        PAYLOAD = {
            "username": "testuser",
            "password": "badpass",
        }

        res = self.client.post(LOGIN_URL, PAYLOAD)
        res_status = res.data["status"]
        res_data = res.data["data"]
        tokens = res_data["tokens"]

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(res_status, "success")
        self.assertIn("access", tokens)
        self.assertIn("refresh", tokens)
