from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from apps.position.models import Position
from apps.team.models import Team


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position, null=True, blank=True, on_delete=models.SET_NULL
    )
    team = models.ForeignKey(
        Team,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    is_manager = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("worker:worker-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
