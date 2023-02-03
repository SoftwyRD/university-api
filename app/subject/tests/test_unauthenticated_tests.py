from django.test import TestCase
from core.models import Subject as SubjectModel
from rest_framework.reverse import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, force_authenticate
from rest_framework import status

SUBJECT_URL = reverse("subject:subject-list")


# Create your tests here.
class SubjectUnauthenticatedTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_create_subject_test_success(self) -> None:
        res = self.client.get(SUBJECT_URL)
        print(res.status_code)

        self.assertEqual(1, status.HTTP_200_OK)
