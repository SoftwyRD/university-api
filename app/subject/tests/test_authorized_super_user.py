"""Test cases for authorized super user."""

from django.contrib.auth import get_user_model

from rest_framework.test import APIClient, APITestCase
from rest_framework.reverse import reverse
from rest_framework import status

SUBJECTS_URL = reverse("subject:subject-list")


def detail_url(id):
    """Get reverse url for subject details"""

    return reverse("subject:subject-detail", args=[id])


class AuthorizedTests(APITestCase):
    """Test cases for authorized super user."""

    payload = {
        "code": "IDS222",
        "name": "Desarrollo de Software 1",
        "credits": 4,
        "is_lab": 0,
    }

    def setUp(self):
        """Set up test client and super user."""

        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            first_name="first name",
            last_name="last name",
            username="username",
            email="username@example.com",
            password="password",
        )

        self.client.force_authenticate(self.user)

    def test_get_subject(self):
        """Test that super user can get subjects"""

        res = self.client.get(SUBJECTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_subject(self):
        """Test that super user can create a subject"""

        res = self.client.post(SUBJECTS_URL, self.payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn("Location", res)

    def test_create_subject_with_repeated_code(self):
        """Test that super user can't create a subject with repeated code"""

        res1 = self.client.post(SUBJECTS_URL, self.payload)
        res2 = self.client.post(SUBJECTS_URL, self.payload)

        self.assertEqual(res1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_created_subject_by_code(self):
        """Test that super user can get a subject by code"""

        subject = self.client.post(SUBJECTS_URL, self.payload)

        res = self.client.get(
            detail_url(subject.data["data"]["subject"]["id"])
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            res.data["data"]["subject"]["name"],
            subject.data["data"]["subject"]["name"],
        )

    def test_get_unexisting_subject(self):
        """Test that super user can't get an unexisting subject"""

        res = self.client.get(detail_url(1))

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_existing_subject(self):
        """Test that super user can delete a subject"""

        subject = self.client.post(SUBJECTS_URL, self.payload)

        res = self.client.delete(
            detail_url(subject.data["data"]["subject"]["id"])
        )

        res1 = self.client.get(
            detail_url(subject.data["data"]["subject"]["id"])
        )

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(res1.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_unexisting_subject(self):
        """Test that super user can't delete an unexisting subject"""

        res = self.client.delete(detail_url(1))

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_existing_subject(self):
        """Test that super user can patch a subject"""

        subject = self.client.post(SUBJECTS_URL, self.payload)

        payload = {
            "code": "IDS224",
            "name": "Desarrollo de Software 3",
            "credits": 4,
            "is_lab": 0,
        }

        res = self.client.patch(
            detail_url(subject.data["data"]["subject"]["id"]), payload
        )

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_patch_unexisting_subject(self):
        """Test that super user can't patch an unexisting subject"""

        payload = {
            "code": "IDS224",
            "name": "Desarrollo de Software 3",
            "credits": 4,
            "is_lab": 0,
        }

        res = self.client.patch(detail_url(1), payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
