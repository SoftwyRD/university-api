from django.contrib.auth import get_user_model
from django.test import TestCase
from core.models import Selection, Subject, SubjectSection

PAYLOAD = {
    "section": 3,
    "professor": "Samuel",
    "taken": False,
}


def create_selection_section(**params):
    selection_section = SubjectSection.objects.create(**params)
    return selection_section


class SelectionSectionModelTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            first_name="Test",
            last_name="User",
            username="testuser",
            email="testuser@example.com",
            password="testpass123",
        )
        self.selection = Selection.objects.create(
            name="My Selection",
            user=self.user,
        )
        self.subject = Subject.objects.create(
            code="TST101",
            name="Test Subject",
            credits=2,
            is_lab=False,
        )
        PAYLOAD.update(
            {
                "selection": self.selection,
                "subject": self.subject,
            }
        )

    def test_create_selection_section_success(self):
        selection_section = create_selection_section(**PAYLOAD)

        self.assertEqual(selection_section.selection, PAYLOAD["selection"])
        self.assertEqual(selection_section.section, PAYLOAD["section"])
        self.assertEqual(selection_section.subject, PAYLOAD["subject"])
        self.assertEqual(selection_section.professor, PAYLOAD["professor"])
        self.assertEqual(selection_section.taken, PAYLOAD["taken"])

    def test_partial_update_selection_section(self):
        new_professor = "Michael"
        selection_section = create_selection_section(**PAYLOAD)
        SubjectSection.objects.update(professor=new_professor)
        selection_section.refresh_from_db()

        self.assertEqual(selection_section.selection, PAYLOAD["selection"])
        self.assertEqual(selection_section.section, PAYLOAD["section"])
        self.assertEqual(selection_section.subject, PAYLOAD["subject"])
        self.assertEqual(selection_section.professor, new_professor)
        self.assertEqual(selection_section.taken, PAYLOAD["taken"])

    def test_delete_selection_section(self):
        selection_section = create_selection_section(**PAYLOAD)
        selection_section.delete()
        selection_section = SubjectSection.objects.filter(
            professor=PAYLOAD["professor"]
        )

        self.assertFalse(selection_section)

    def test_get_selection_section(self):
        create_selection_section(**PAYLOAD)
        selection_section = SubjectSection.objects.get(
            professor=PAYLOAD["professor"]
        )

        self.assertTrue(selection_section)

    def test_get_all_selection_sections(self):
        create_selection_section(**PAYLOAD)

        PAYLOAD.update(
            {
                "section": 1,
                "professor": "Michael",
                "taken": True,
                "subject": self.subject,
                "selection": self.selection,
            }
        )
        create_selection_section(**PAYLOAD)

        selection_sections = SubjectSection.objects.all()

        self.assertEqual(selection_sections.count(), 2)
