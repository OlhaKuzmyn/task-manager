from django.contrib.auth.models import AbstractUser
from django.db import models


class Position(models.Model):
    name = models.CharField(max_length=255)


class Project(models.Model):
    name = models.CharField(max_length=255)


class Team(models.Model):
    name = models.CharField(max_length=255)
    projects = models.ManyToManyField(Project, blank=True, related_name="teams")


class Worker(AbstractUser):
    position = models.ForeignKey(Position, default="Employee" , on_delete=models.SET_DEFAULT)
    is_manager = models.BooleanField(default=False)
    team = models.ForeignKey(Team, null=True, on_delete=models.SET_NULL)


class TaskType(models.Model):
    name = models.CharField(max_length=255)


class Task(models.Model):
    PRIORITY_CHOICES = {
        "UR": "URGENT",
        "HI": "HIGH",
        "ME": "MEDIUM",
        "LO": "LOW",
    }

    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=255, choices=PRIORITY_CHOICES.items())
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    assignees = models.ManyToManyField(Worker, blank=True, related_name="tasks")
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
