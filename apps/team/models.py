from django.db import models

from apps.project.models import Project


class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    projects = models.ManyToManyField(Project, blank=True, related_name="teams")

    def __str__(self):
        return self.name
