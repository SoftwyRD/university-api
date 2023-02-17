"""Test unauthenticated user requests"""

from django.test import TestCase
from core.models import Subject as SubjectModel
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from rest_framework import status

SUBJECT_URL = reverse("subject:subject-list")


def detail_url(id):
    """Get reverse url for subject details"""

    return reverse("subject:subject-detail", args=[id])


class SubjectUnauthenticatedTests(TestCase):
    """Test cases for unauthenticated user."""

    def setUp(self) -> None:
        """Set up test client"""

        self.client = APIClient()

    def test_create_subject_test(self) -> None:
        """Test that unauthenticated user can't create a subject"""

        payload = {
            "code": "IDS222",
            "name": "Desarrollo de Software 1",
            "credits": 4,
            "is_lab": 0,
        }
        res = self.client.post(SUBJECT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_subject_test_success(self) -> None:
        """Test that unauthenticated user can get subjects"""

        SubjectModel.objects.create(
            code="IDS222",
            name="Desarrollo de Software 1",
            credits=4,
            is_lab=0,
        )

        res = self.client.get(SUBJECT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_subject(self):
        """Test that unauthenticated user can't delete a subject"""

        res = self.client.delete(detail_url(1))

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_subject(self):
        """Test that unauthenticated user can't patch a subject"""

        res = self.client.patch(detail_url(1))

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
