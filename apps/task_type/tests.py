from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.task_type.models import TaskType

TASK_TYPE_URL = reverse("task_type:task-type-list")


class TestTaskTypeSearch(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="worker_test_user",
            password="test1234"
        )
        self.client.force_login(self.user)

    def test_task_type_search(self):
        TaskType.objects.create(
            name="Test Task Type",
        )
        TaskType.objects.create(
            name="New Task Type",
        )
        TaskType.objects.create(
            name="New Task Type 1",
        )
        response = self.client.get(TASK_TYPE_URL)
        self.assertEqual(response.status_code, 200)
        new_task_types = TaskType.objects.filter(name__icontains="new")
        response_query = self.client.get(
            TASK_TYPE_URL,
            {"name": "new"}
        )
        self.assertEqual(response_query.status_code, 200)
        self.assertEqual(
            list(new_task_types),
            list(response_query.context['task_type_list']),
        )
