from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.test import TestCase
from django.urls import reverse

from apps.project.models import Project

PROJECT_CREATE_URL = reverse("project:project-create")
PROJECT_LIST_URL = reverse("project:project-list")


class TestProjectView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="manager_user",
            password="test1234"
        )
        self.manager_group = Group.objects.get(name="Manager")
        self.manager_group.permissions.set(
            Permission.objects.filter(
                codename__in=["add_project"]
            )
        )
        self.user.groups.add(self.manager_group)
        self.user.is_manager = True
        self.user.save()
        self.client.force_login(self.user)

    def test_project_creation(self):
        form_data = {
            "name": "Test Project",
        }
        response = self.client.post(
            PROJECT_CREATE_URL, data=form_data
        )
        self.assertEqual(response.status_code, 302)

    def test_pagination_five(self):
        for i in range(15):
            Project.objects.create(
                name="Test Project {}".format(i),
            )

        response = self.client.get(PROJECT_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["project_list"]), 5)
