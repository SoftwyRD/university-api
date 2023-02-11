from django.test import TestCase
from core.models import Subject as SubjectModel
# from subject.serializers import SubjectSerializer
from rest_framework.reverse import reverse
# from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

SUBJECT_URL = reverse("subject:subject-list")


def detail_url(id):
    return reverse('subject:subject-detail', args=[id])


class SubjectUnauthenticatedTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_create_subject_test(self) -> None:
        payload = {
            'code': 'IDS222',
            'name': 'Desarrollo de Software 1',
            'credits': 4,
            'is_lab': 0,
        }
        res = self.client.post(SUBJECT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_subject_test_success(self) -> None:

        SubjectModel.objects.create(
            code='IDS222',
            name='Desarrollo de Software 1',
            credits=4,
            is_lab=0,
        )

        res = self.client.get(SUBJECT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_subject(self):
        res = self.client.delete(detail_url("111111"))

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_subject(self):
        res = self.client.patch(detail_url("111111"))

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
