from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.reverse import reverse

from core.models import Selection as SelectionModel
from schedule.serializers import SelectionSerializer

SELECTION_URL = reverse("schedule:selection-list")


def selection_detail_url(id):
    return reverse("schedule:selection-detail", args=[id])


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


class SelectionTestsUnaythorized(APITestCase):
    payload = {
        "name": "name",
    }

    def setUp(self):
        self.client = APIClient()

    def test_post_selection(self):
        res = self.client.post(SELECTION_URL, self.payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_selection(self):
        res = self.client.get(SELECTION_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class SelectionTestsAuthorized(APITestCase):
    payload = {
        "name": "selection name",
    }

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()

        self.client.force_authenticate(self.user)

    def test_get_empty_selection(self):
        res = self.client.get(SELECTION_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_post_selection(self):
        payload = {
            "name": "new name",
        }

        res = self.client.post(SELECTION_URL, payload)

        # print(res.data["data"]["selection"])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["data"]["selection"]
                         ["name"], payload["name"])
        self.assertEqual(res.data["data"]["selection"]
                         ["user"], self.user.id)

    def test_post_selection_different_users(self):
        payload = {
            "name": "new name",
        }
        newUser = create_user(email="newmail@example.com",
                              username='newsuusername')
        SelectionModel.objects.create(
            user=newUser, name="other user selection")

        resSelection = self.client.post(SELECTION_URL, payload)

        res = self.client.get(SELECTION_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(resSelection.data["data"]["selection"]
                         ["user"], res.data["data"]["selections"][0]
                         ["user"])
        self.assertEqual(resSelection.data["data"]["selection"]
                         ["name"], res.data["data"]["selections"][0]
                         ["name"])

    def test_post_selection_same_names(self):
        self.client.post(SELECTION_URL, self.payload)
        self.client.post(SELECTION_URL, self.payload)

        res = self.client.get(SELECTION_URL)

        self.assertEqual(len(res.data), 2)

    def test_get_one_selection(self):
        selection = self.client.post(SELECTION_URL, self.payload)

        id = selection.data["data"]["selection"]["id"]

        res = self.client.get(selection_detail_url(id))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["data"]["selection"]["id"],
                         selection.data["data"]["selection"]["id"])

    def test_cant_get_selection_of_other_user(self):
        self.client.post(SELECTION_URL, self.payload)

        newUser = create_user(email="newmail@example.com",
                              username='newsuusername')
        otherSelection = SelectionModel.objects.create(
            user=newUser, name="other user selection")

        id = otherSelection.id

        res = self.client.get(selection_detail_url(id))
        print(res.data)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
