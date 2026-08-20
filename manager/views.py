from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from manager.models import Task, Project, Team, Worker, Position, TaskType


def index(request):
    """Introductory view with not completed Tasks, Projects, Teams and workers count"""

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


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    queryset = Task.objects.select_related("project")
    paginate_by = 5


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    queryset = Worker.objects.select_related("position")
    paginate_by = 5


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker

# add manager permission to worker?
# different update for manager and for worker
# worker to be able to update only themselves
# manager being able to update all workers

class ProjectListView(LoginRequiredMixin, generic.ListView):
    model = Project
    paginate_by = 5


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    model = Project


class ProjectCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Project
    fields = "__all__"
    permission_required = "projects.add_project"

    def get_success_url(self):
        return reverse_lazy("manager:project-detail", kwargs={"pk": self.object.pk})


class ProjectUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = Project
    fields = "__all__"
    permission_required = "projects.change_project"

    def get_success_url(self):
        return reverse_lazy("manager:project-detail", kwargs={"pk": self.object.pk})


class ProjectDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = Project
    permission_required = "projects.delete_project"
    success_url = reverse_lazy("manager:project-list")


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    paginate_by = 5


class PositionCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Position
    fields = "__all__"
    permission_required = "positions.add_position"
    success_url = reverse_lazy("manager:position-list")


class PositionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = Position
    fields = "__all__"
    permission_required = "positions.change_position"
    success_url = reverse_lazy("manager:position-list")

class PositionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = Position
    permission_required = "positions.delete_position"
    success_url = reverse_lazy("manager:position-list")

class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    paginate_by = 5
    template_name = "manager/task_type_list.html"
    context_object_name = "task_type_list"

class TaskTypeCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = TaskType
    fields = "__all__"
    permission_required = "tasktypes.add_tasktype"
    template_name = "manager/task_type_form.html"
    success_url = reverse_lazy("manager:task-type-list")

class TaskTypeUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = TaskType
    fields = "__all__"
    permission_required = "tasktypes.change_tasktype"
    template_name = "manager/task_type_form.html"
    success_url = reverse_lazy("manager:task-type-list")

class TaskTypeDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = TaskType
    permission_required = "tasktypes.delete_tasktype"
    template_name = "manager/task_type_confirm_delete.html"
    success_url = reverse_lazy("manager:task-type-list")


class TeamListView(LoginRequiredMixin, generic.ListView):
    model = Team
    paginate_by = 5


class TeamDetailView(LoginRequiredMixin, generic.DetailView):
    model = Team
# add worker to a team through team view or user view
# or create separate forms and views and/or forms for manager user edit and regular user edit

class TeamCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Team
    fields = "__all__"
    permission_required = "teams.add_team"

    def get_success_url(self):
        return reverse_lazy("manager:team-detail", kwargs={"pk": self.object.pk})


class TeamUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = Team
    fields = "__all__"
    permission_required = "teams.change_team"

    def get_success_url(self):
        return reverse_lazy("manager:team-detail", kwargs={"pk": self.object.pk})


class TeamDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = Team
    permission_required = "teams.delete_team"
    success_url = reverse_lazy("manager:team-list")

