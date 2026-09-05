import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.project.models import Project
from apps.task.models import Task
from apps.task_type.models import TaskType


TASK_LIST_URL = reverse("task:task-list")


class TestTaskList(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="manager_user",
            password="test1234"
        )
        self.client.force_login(self.user)

    def test_task_search(self):
        test_type = TaskType.objects.create(
            name="Test Task Type",
        )
        project = Project.objects.create(
            name="Test Project",
        )
        Task.objects.create(
            name="Task 1",
            deadline=datetime.datetime.now(),
            priority=1,
            task_type=test_type,
            project=project,
        )
        Task.objects.create(
            name="Task 2",
            deadline=datetime.datetime.now(),
            priority=1,
            task_type=test_type,
            project=project,
        )
        Task.objects.create(
            name="Task 3",
            deadline=datetime.datetime.now(),
            priority=1,
            task_type=test_type,
            project=project,
        )
        response = self.client.get(TASK_LIST_URL)
        self.assertEqual(response.status_code, 200)

        Task.objects.get(name="Task 1").assignees.add(self.user)
        Task.objects.get(name="Task 2").assignees.add(self.user)

        tasks_user_test = Task.objects.filter(
            assignees=self.user,
        )
        response_query = self.client.get(TASK_LIST_URL, {"filter_select": "mine"})
        self.assertEqual(response_query.status_code, 200)
        self.assertEqual(
            list(tasks_user_test),
            list(response_query.context["task_list"])
        )
