from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


POSITION_CREATION_URL = reverse("position:position-create")


class TestPositionUserNonManager(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="worker_test_user",
            password="test1234"
        )
        self.client.force_login(self.user)

    def test_position_creation_not_possible(self):
        form_data = {
            "name": "Test Position",
        }
        response = self.client.post(
            POSITION_CREATION_URL,
            data=form_data
        )
        self.assertEqual(response.status_code, 403)
