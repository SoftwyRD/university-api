from django.test import TestCase
from core.models import Weekday

PAYLOAD = {
    "name": "Monday",
}


def create_weekday(**params):
    weekday = Weekday.objects.create(**params)
    return weekday


class WeekdayModelTests(TestCase):
    def test_create_weekday_success(self):
        weekday = create_weekday(**PAYLOAD)

        self.assertEqual(weekday.name, PAYLOAD["name"])

    def test_partial_update_weekday(self):
        new_name = "Mondayn't"
        weekday = create_weekday(**PAYLOAD)
        Weekday.objects.update(name=new_name)
        weekday.refresh_from_db()

        self.assertEqual(weekday.name, new_name)

    def test_delete_weekday(self):
        weekday = create_weekday(**PAYLOAD)
        weekday.delete()
        weekday = Weekday.objects.filter(name=PAYLOAD["name"])

        self.assertFalse(weekday)

    def test_get_weekday(self):
        create_weekday(**PAYLOAD)
        weekday = Weekday.objects.get(name=PAYLOAD["name"])

        self.assertTrue(weekday)

    def test_get_all_weekdays(self):
        create_weekday(**PAYLOAD)

        PAYLOAD.update(
            {
                "name": "Tuesday",
            }
        )
        create_weekday(**PAYLOAD)

        weekdays = Weekday.objects.all()

        self.assertEqual(weekdays.count(), 2)
