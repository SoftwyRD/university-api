"""Weekday model tests."""

from django.test import TestCase
from core.models import Weekday

PAYLOAD = {
    "name": "Monday",
}


def create_weekday(**params):
    """Helper function to create a weekday"""

    weekday = Weekday.objects.create(**params)
    return weekday


class WeekdayModelTests(TestCase):
    """Test weekday model"""

    def test_create_weekday_success(self):
        """Test creating a weekday"""

        weekday = create_weekday(**PAYLOAD)

        self.assertEqual(weekday.name, PAYLOAD["name"])

    def test_partial_update_weekday(self):
        """Test updating a weekday"""

        new_name = "Mondayn't"
        weekday = create_weekday(**PAYLOAD)
        Weekday.objects.update(name=new_name)
        weekday.refresh_from_db()

        self.assertEqual(weekday.name, new_name)

    def test_delete_weekday(self):
        """Test deleting a weekday"""

        weekday = create_weekday(**PAYLOAD)
        weekday.delete()
        weekday = Weekday.objects.filter(name=PAYLOAD["name"])

        self.assertFalse(weekday)

    def test_get_weekday(self):
        """Test getting a weekday"""

        create_weekday(**PAYLOAD)
        weekday = Weekday.objects.get(name=PAYLOAD["name"])

        self.assertTrue(weekday)

    def test_get_all_weekdays(self):
        """Test getting all weekdays"""

        create_weekday(**PAYLOAD)

        PAYLOAD.update(
            {
                "name": "Tuesday",
            }
        )
        create_weekday(**PAYLOAD)

        weekdays = Weekday.objects.all()

        self.assertEqual(weekdays.count(), 2)
