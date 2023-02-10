from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.reverse import reverse

from core.models import Selection as SelectionModel
from datetime import datetime
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

    def test_get_selections(self):
        res = self.client.get(SELECTION_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_selection(self):
        res = self.client.get(selection_detail_url(0))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_selection(self):
        res = self.client.delete(selection_detail_url(0))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_selection(self):
        res = self.client.patch(selection_detail_url(0))
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
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_one_selection(self):
        selection = self.client.post(SELECTION_URL, self.payload)

        id = selection.data["data"]["selection"]["id"]

        res = self.client.delete(selection_detail_url(id))

        selectionsNumber = SelectionModel.objects.all().count()

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(selectionsNumber, 0)

    def test_delete_deleted_selection(self):
        selection = self.client.post(SELECTION_URL, self.payload)

        id = selection.data["data"]["selection"]["id"]

        self.client.delete(selection_detail_url(id))
        res = self.client.delete(selection_detail_url(id))

        selectionsNumber = SelectionModel.objects.all().count()

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(selectionsNumber, 0)

    def test_delete_other_user_selection(self):
        newUser = create_user(email="newmail@example.com",
                              username='newsuusername')
        otherSelection = SelectionModel.objects.create(
            user=newUser, name="other user selection")

        id = otherSelection.id

        res = self.client.delete(selection_detail_url(id))

        selectionsNumber = SelectionModel.objects.all().count()

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(selectionsNumber, 1)

    def test_patch_selection(self):
        selection = SelectionModel.objects.create(
            user=self.user, name="my selection")
        id = selection.id

        payload = {
            "name": "my super new name",
        }
        res = self.client.patch(selection_detail_url(id), payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["data"]["selection"]
                         ["name"], payload["name"])

    def test_patch_selection_change_id_unsuccess(self):
        selection = SelectionModel.objects.create(
            user=self.user, name="my selection")
        id = selection.id

        payload = {
            "id": 2,
        }
        res = self.client.patch(selection_detail_url(id), payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(str(id), res.data["data"]["selection"]
                         ["id"])

    def test_patch_selection_of_other_user(self):
        SelectionModel.objects.create(
            user=self.user, name="my selection")

        newUser = create_user(email="newmail@example.com",
                              username='newsuusername')
        otherSelection = SelectionModel.objects.create(
            user=newUser, name="other user selection")

        idOther = otherSelection.id

        payload = {
            "name": "other user name",
        }
        res = self.client.patch(selection_detail_url(idOther), payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_selection_data_modified_succesfully(self):
        selection = SelectionModel.objects.create(
            user=self.user,
            name="my selection")

        id = selection.id

        self.assertEqual(selection.created_on, selection.modified_on)
        payload = {
            "name": "my super new name",
        }

        res = self.client.patch(selection_detail_url(id), payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        createdTimeInRes = res.data["data"]["selection"]["created_on"]

        date_object = datetime.strptime(
            createdTimeInRes, '%Y-%m-%dT%H:%M:%S.%fZ')

        self.assertEqual(date_object.strftime(
            '%Y-%m-%dT%H:%M:%S.%fZ'),
            selection.created_on.strftime('%Y-%m-%dT%H:%M:%S.%fZ'))

        self.assertNotEqual(res.data["data"]["selection"]
                            ["modified_on"], selection.modified_on)
        self.assertNotEqual(res.data["data"]["selection"]
                            ["created_on"], res.data["data"]["selection"]
                            ["modified_on"])