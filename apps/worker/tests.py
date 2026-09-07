from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.test import TestCase
from django.urls import reverse

from apps.position.models import Position
from apps.team.models import Team

WORKER_CREATE_URL = reverse("worker:worker-create")


class TestWorkerManagerView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="manager_user",
            password="test1234"
        )
        self.manager_group = Group.objects.get(name="Manager")
        self.manager_group.permissions.set(
            Permission.objects.filter(
                codename__in=["add_worker", "change_worker"]
            )
        )
        self.user.groups.add(self.manager_group)
        self.user.is_manager = True
        self.user.save()
        self.client.force_login(self.user)

        test_position = Position.objects.create(name="test_position")
        test_team = Team.objects.create(name="test_team")

        self.form_data = {
            "username": "test_user",
            "password1": "us3r12t@st@new",
            "password2": "us3r12t@st@new",
            "first_name": "Test First",
            "last_name": "Test Last",
            "position": test_position.id,
            "team": test_team.id,
        }


        self.response = self.client.post(
            WORKER_CREATE_URL, data=self.form_data
        )

    def test_worker_creation(self):
        self.assertEqual(self.response.status_code, 302)
        new_user = get_user_model().objects.get(
            username=self.form_data["username"]
        )
        self.assertEqual(
            self.form_data["first_name"], new_user.first_name
        )
        self.assertEqual(
            self.form_data["last_name"], new_user.last_name
        )
        self.assertEqual(
            self.form_data["position"], new_user.position.pk
        )
        self.assertEqual(
            self.form_data["team"], new_user.team.pk
        )

    def test_worker_update_manager(self):
        new_upd_user = get_user_model().objects.get(
            username=self.form_data["username"]
        )
        worker_detail_url = reverse(
            "worker:worker-detail", kwargs={"pk": new_upd_user.id}
        )
        upd_response = self.client.post(worker_detail_url)
        self.assertEqual(upd_response.status_code, 302)

        new_upd_user.refresh_from_db()

        self.assertTrue(
            new_upd_user.groups.filter(name="Manager").exists()
            and new_upd_user.is_manager
        )

    def test_superuser_is_manager(self):
        new_super_user = get_user_model().objects.create_superuser(
            username="superuser_user",
            email="test@test.com",
            password="us3r12t@st@new"

        )
        self.assertTrue(
            new_super_user.groups.filter(name="Manager").exists()
            and new_super_user.is_manager
        )


class TestWorkerNonManagerView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="worker_test_user",
            password="test1234"
        )
        self.client.force_login(self.user)

    def test_worker_creation_not_possible(self):
        form_data = {
            "username": "test_user",
            "password1": "us3r12t@st@new",
            "password2": "us3r12t@st@new",
            "first_name": "Test First",
            "last_name": "Test Last",
        }
        response = self.client.post(WORKER_CREATE_URL, data=form_data)
        self.assertEqual(response.status_code, 403)


class TestModelWorker(TestCase):
    def test_get_absolute_url(self):
        new_user = get_user_model().objects.create_user(
            username="user",
            password="usermodel1234"
        )
        self.assertEqual(new_user.get_absolute_url(), f"/workers/{new_user.id}/")
