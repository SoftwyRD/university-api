"""Test selection model"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from core.models import Selection

PAYLOAD = {
    "name": "Test Subject",
}


def create_selection(**params):
    """Helper function to create a selection"""

    selection = Selection.objects.create(**params)
    return selection


def create_user(**params):
    """Helper function to create a user"""

    defauls = {
        "first_name": "Test",
        "last_name": "User",
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpass123",
    }
    defauls.update(**params)
    user = get_user_model().objects.create(**defauls)
    return user


class SubjectModelTests(TestCase):
    """Test selection model"""

    def setUp(self) -> None:
        """Create a user"""

        user = create_user()
        PAYLOAD.update({"user": user})

    def test_create_selection_success(self):
        """Test creating a selection"""

        selection = create_selection(**PAYLOAD)

        self.assertEqual(selection.name, PAYLOAD["name"])
        self.assertEqual(selection.user, PAYLOAD["user"])

    def test_partial_update_selection(self):
        """Test updating a selection"""

        new_name = "Another selection"
        selection = create_selection(**PAYLOAD)
        Selection.objects.update(name=new_name)
        selection.refresh_from_db()

        self.assertEqual(selection.name, PAYLOAD["name"])
        self.assertEqual(selection.user, PAYLOAD["user"])

    def test_delete_selection(self):
        """Test deleting a selection"""

        selection = create_selection(**PAYLOAD)
        selection.delete()
        selection = Selection.objects.filter(name=PAYLOAD["name"])

        self.assertFalse(selection)

    def test_get_selection(self):
        """Test getting a selection"""

        create_selection(**PAYLOAD)
        selection = Selection.objects.get(name=PAYLOAD["name"])

        self.assertTrue(selection)

    def test_get_all_selections(self):
        """Test getting all selections"""

        create_selection(**PAYLOAD)

        PAYLOAD.update({"name": "Another selection"})
        create_selection(**PAYLOAD)

        selections = Selection.objects.all()

        self.assertEqual(selections.count(), 2)
