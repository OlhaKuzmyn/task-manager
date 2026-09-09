from django.contrib.auth import get_user_model
from django.shortcuts import render

from apps.project.models import Project
from apps.task.models import Task
from apps.team.models import Team


def index(request):
    """Introductory view with not completed
    Tasks, Projects, Teams and workers count"""

    num_tasks_not_completed = Task.objects.filter(is_completed=False).count()
    num_projects = Project.objects.count()
    num_teams = Team.objects.count()
    num_workers = get_user_model().objects.count()

    context = {
        "num_tasks_not_completed": num_tasks_not_completed,
        "num_projects": num_projects,
        "num_teams": num_teams,
        "num_workers": num_workers,
    }

    return render(request, "manager/index.html", context=context)
