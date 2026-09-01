from django.db import models

from apps.project.models import Project
from apps.task_type.models import TaskType
from apps.worker.models import Worker


class Task(models.Model):

    class Priority(models.IntegerChoices):
        URGENT = 0, "Urgent"
        HIGH = 1, "High"
        MEDIUM = 2, "Medium"
        LOW = 3, "Low"

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    priority = models.IntegerField(choices=Priority.choices)
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    assignees = models.ManyToManyField(Worker, blank=True, related_name="tasks")
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["priority"]
