from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

# Create your tests here.

USER_URL = reverse("user")
LOGIN_URL = reverse("user:login")


class PublicUserApiTests(TestCase):
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
            "username": "not_an_valid_user",
            "password": "not_a_valid_password",
        }

        res = self.client.post(LOGIN_URL, PAYLOAD)
        res_status = res.data["status"]
        res_data = res.data["data"]

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(res_status, "fail")
        self.assertNotIn("tokens", res_data)
        self.assertIn("title", res_data)
        self.assertIn("message", res_data)


class PrivateUserApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

        self.PAYLOAD = {
            "first_name": "Test",
            "last_name": "User",
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpass123",
        }
        self.user = get_user_model().objects.create(**self.PAYLOAD)

    def test_login_success(self):
        PAYLOAD = {
            "username": self.PAYLOAD["username"],
            "password": self.PAYLOAD["password"],
        }

        res = self.client.post(LOGIN_URL, PAYLOAD)
        data = res.data
        res_status = data["status"]
        res_data = data["data"]
        tokens = res_data["tokens"]

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertIn("status", data)
        self.assertEqual(res_status, "success")

        self.assertIn("data", data)
        self.assertIn("tokens", res_data)

        self.assertIn("access", tokens)
        self.assertIn("refresh", tokens)
