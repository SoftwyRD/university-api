from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

# Create your tests here.

LOGIN_URL = reverse("user:pair-token")
LOGIN_REFRESH_URL = reverse("user:refresh-token")
USER_LIST_URL = reverse("user:list")
USER_DETAILS_URL = reverse("user:details")
ME_URL = reverse("user:me")


def user_detail_url(user_id):
    return reverse("user:detail", args=[user_id])


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
        data = res.data

        res_status = data["status"]
        res_data = data["data"]
        user = res_data["user"]

        user_location = f"/api/users/{user.id}/"

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res["Location"], user_location)

        self.assertIn("status", data)
        self.assertEqual(res_status, "success")

        self.assertIn("data", data)
        self.assertIn("user", res_data)

        self.assertNotIn("password", user)
        self.assertEqual(user["username"], PAYLOAD["username"])

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

    def test_login_not_registered(self):
        PAYLOAD = {
            "username": "not_an_valid_user",
            "password": "not_a_valid_password",
        }

        res = self.client.post(LOGIN_URL, PAYLOAD)
        data = res.data

        res_status = data["status"]
        res_data = data["data"]

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

        self.assertIn("status", data)
        self.assertEqual(res_status, "fail")

        self.assertIn("data", data)
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

    def test_retrieve_profile_success(self):
        res = self.client.get(ME_URL)
        data = res.data

        res_status = data["status"]
        res_data = data["data"]
        profile = res_data["profile"]

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertIn("status", data)
        self.assertEqual(res_status, "success")

        self.assertIn("data", data)
        self.assertIn("profile", res_data)

        self.assertIn("first_name", profile)
        self.assertIn("middle_name", profile)
        self.assertIn("last_name", profile)
        self.assertIn("username", profile)
        self.assertIn("email", profile)

        self.assertNotIn("password", profile)


class AdminUserApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

        PAYLOAD = {
            "first_name": "Test",
            "last_name": "User",
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpass123",
        }
        self.admin = get_user_model().objects.create_superuser(**PAYLOAD)
        self.force_authenticate(self.admin)

        PAYLOAD.update(
            {
                "first_name": "Another",
                "middle_name": "User",
                "last_name": "Name",
                "username": "seconduser",
                "email": "seconduser@example.com",
                "password": "testpass123",
            }
        )
        self.user = get_user_model().objects.create(**PAYLOAD)

    def test_get_user(self):
        USER_DETAIL_URL = user_detail_url(self.user.id)

        res = self.client.get(USER_DETAIL_URL)
        data = res.data

        res_status = data["status"]
        res_data = data["data"]
        res_user = res_data["user"]

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertIn("status", data)
        self.assertEqual(res_status, "success")

        self.assertIn("data", data)
        self.assertIn("user", res_data)

        self.assertEqual(res_user["first_name"], self.user["first_name"])
        self.assertEqual(res_user["middle_name"], self.user["middle_name"])
        self.assertEqual(res_user["last_name"], self.user["last_name"])
        self.assertEqual(res_user["username"], self.user["username"])
        self.assertEqual(res_user["email"], self.user["email"])

        self.assertNotIn("password", res_user)

    def test_get_all_users(self):
        users = get_user_model().objects.all()

        USER_DETAIL_URL = user_detail_url(self.user.id)

        res = self.client.get(USER_DETAIL_URL)
        data = res.data

        res_status = data["status"]
        res_data = data["data"]
        res_users = res_data["users"]

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertIn("status", data)
        self.assertEqual(res_status, "success")

        self.assertIn("data", data)
        self.assertIn("count", res_data)
        self.assertEqual(res_data["count"], len(res_users))
        self.assertEqual(len(res_users), len(users))

        self.assertIn("users", res_data)

        for user in res_users:
            self.assertIn("first_name", user)
            self.assertIn("middle_name", user)
            self.assertIn("last_name", user)
            self.assertIn("username", user)
            self.assertIn("email", user)

            self.assertNotIn("password", user)
