from django.test import TestCase

from apps.project.models import Project
from apps.team.forms import TeamSearchForm
from apps.team.models import Team


class TestTeamForm(TestCase):
    def test_team_search_form(self):
        project = Project.objects.create(
            name="Test Project",
        )
        form_data = {
            "name": "test",
            "projects": (str(project.pk),),
        }
        form = TeamSearchForm(form_data)
        self.assertTrue(form.is_valid())


class TestTeamModel(TestCase):
    def test_team_str(self):
        test_team = Team.objects.create(
            name="Test Team",
        )
        self.assertEqual(str(test_team), test_team.name)
