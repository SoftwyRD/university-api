from django.contrib.auth import get_user_model

from rest_framework.test import APIClient, APITestCase
from rest_framework.reverse import reverse
from core.models import User
from rest_framework import status
SUBJECTS_URL = reverse('subject:subject-list')


class AuthorizedTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            first_name='first name',
            last_name='last name',
            username='username',
            email='username@example.com',
            password='password',
        )

        self.client.force_authenticate(self.user)

    def test_get_models(self):
        res = self.client.get(SUBJECTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
