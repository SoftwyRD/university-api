"""Test Schedule Model"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from core.models import (
    SectionSchedule,
    Weekday,
    SubjectSection,
    Selection,
    Subject,
)

PAYLOAD = {
    "start_time": 11,
    "end_time": 13,
}


def create_schedule(**params):
    """Helper function to create a schedule"""

    schedule = SectionSchedule.objects.create(**params)
    return schedule


class ScheduleModelTests(TestCase):
    """Test Schedule Model"""

    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            first_name="Test",
            last_name="User",
            username="testuser",
            email="testuser@example.com",
            password="testpass123",
        )
        """Create a subject, selection, section, and weekday"""

        self.subject = Subject.objects.create(
            code="TST101",
            name="Test Subject",
            credits=2,
            is_lab=False,
        )
        self.selection = Selection.objects.create(
            name="My Selection",
            user=self.user,
        )
        self.section = SubjectSection.objects.create(
            selection=self.selection,
            section=2,
            subject=self.subject,
            professor="Michael",
            taken=True,
        )
        self.weekday = Weekday.objects.create(name="Monday")

        PAYLOAD.update(
            {
                "section": self.section,
                "weekday": self.weekday,
            }
        )

    def test_create_schedule_success(self):
        """Test that a schedule can be created"""

        schedule = create_schedule(**PAYLOAD)

        self.assertEqual(schedule.section, PAYLOAD["section"])
        self.assertEqual(schedule.weekday, PAYLOAD["weekday"])
        self.assertEqual(schedule.start_time, PAYLOAD["start_time"])
        self.assertEqual(schedule.end_time, PAYLOAD["end_time"])

    def test_partial_update_schedule(self):
        """Test that a schedule can be partially updated"""

        new_weekday = Weekday.objects.create(name="Tuesday")
        schedule = create_schedule(**PAYLOAD)
        SectionSchedule.objects.update(weekday=new_weekday)
        schedule.refresh_from_db()

        self.assertEqual(schedule.section, PAYLOAD["section"])
        self.assertEqual(schedule.weekday, new_weekday)
        self.assertEqual(schedule.start_time, PAYLOAD["start_time"])
        self.assertEqual(schedule.end_time, PAYLOAD["end_time"])

    def test_delete_schedule(self):
        """Test that a schedule can be deleted"""

        schedule = create_schedule(**PAYLOAD)
        schedule.delete()
        schedule = SectionSchedule.objects.filter(weekday=PAYLOAD["weekday"])

        self.assertFalse(schedule)

    def test_get_schedule(self):
        """Test that a schedule can be retrieved"""

        create_schedule(**PAYLOAD)
        schedule = SectionSchedule.objects.get(weekday=PAYLOAD["weekday"])

        self.assertTrue(schedule)

    def test_get_all_schedules(self):
        """Test that all schedules can be retrieved"""

        create_schedule(**PAYLOAD)
        weekday = Weekday.objects.create(name="Friday")

        PAYLOAD.update({"weekday": weekday})
        create_schedule(**PAYLOAD)

        schedules = SectionSchedule.objects.all()

        self.assertEqual(schedules.count(), 2)
