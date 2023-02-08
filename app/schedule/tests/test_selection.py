from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.reverse import reverse

from core.models import Selection as SelectionModel

SELECTION_URL = reverse("schedule:selection-list")


def create_user(first_name="first_name",
                last_name="last_name",
                email="user@example.com",
                username="username",
                password="password"):
    data = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "username": username,
        "password": password,
    }
    user = get_user_model().objects.create(**data)
    return user


class SelectionTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()

        self.client.force_authenticate(self.user)

    def test_get_empty_selection(self):
        # SelectionModel.objects.create(name="Name", user=self.user)
        res = self.client.get(SELECTION_URL)
        # print(res.data["data"]["selection"])

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_post_selection(self):
        payload = {
            "name": "name",
        }

        res = self.client.post(SELECTION_URL, payload)

        selections = SelectionModel.objects.all()
        # res2 = self.client.get(SELECTION_URL)
        # print(res.data["data"]["selection"])
        # print(selections)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
