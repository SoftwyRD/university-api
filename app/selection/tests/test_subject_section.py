from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase
from core.models import (
    Selection as SelectionModel,
    Subject as SubjectModel,
    SubjectSection as SubjectSectionModel,
)


def subject_section_url(selection_id, subject_section_id):
    return reverse(
        "selection:subject-detail", args=[selection_id, subject_section_id]
    )


def create_user(**payload):
    defaults = {
        "first_name": "first_name",
        "last_name": "last_name",
        "email": "email@example.com",
        "username": "username",
        "password": "password123",
    }
    defaults.update(payload)
    user = get_user_model().objects.create(**defaults)
    return user


class SubjectSectionPublicAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = create_user()
        self.subject = SubjectModel.objects.create(
            code="TST123", name="Test subject", credits=4, is_lab=False
        )
        self.selection = SelectionModel.objects.create(
            name="My Selection", user=self.user
        )
        self.subject_section = SubjectSectionModel.objects.create(
            subject=self.subject,
            selection=self.selection,
            section=1,
            professor="Marco Antonio",
            taken=True,
        )

        self.payload = {
            "selection": self.selection.id,
            "section": 1,
            "subject": self.subject.id,
            "professor": "Marco Antonio",
            "taken": True,
        }
        self.client.force_authenticate(user=self.user)

    def test_retireve_subject_sections(self):
        """Test that the subject sections can be retrieved"""
        res = self.client.get(
            reverse("selection:subject-list", args=[self.selection.id])
        )
        data = res.data

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("status", data)
        self.assertIn("data", data)
        self.assertIn("count", data["data"])
        self.assertIn("subject_sections", data["data"])

    def test_create_subject_section(self):
        """Test that the subject section can be created"""
        res = self.client.post(
            reverse("selection:subject-list", args=[self.selection.id]),
            self.payload,
            format="json",
        )
        data = res.data

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn("status", data)
        self.assertIn("data", data)
        self.assertIn("subject_section", data["data"])

    def test_update_subject_section(self):
        """Test that the subject section can be updated"""
        res = self.client.patch(
            subject_section_url(self.selection.id, self.subject_section.id),
            self.payload,
            format="json",
        )
        data = res.data

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("status", data)
        self.assertIn("data", data)
        self.assertIn("subject_section", data["data"])

    def test_delete_subject_section(self):
        """Test that the subject section can be deleted"""
        res = self.client.delete(
            subject_section_url(self.selection.id, self.subject_section.id)
        )
        data = res.data

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(data, None)
