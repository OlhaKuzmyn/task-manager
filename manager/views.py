from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import PasswordChangeView
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from manager.forms import (
    TaskSearchForm,
    TaskForm,
    WorkerCreationForm,
    WorkerUpdateForm,
    # TeamUpdateForm,
    WorkerSearchForm,
    PositionSearchForm,
    TeamSearchForm,
    TaskTypeSearchForm
)
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
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        deadline = self.request.GET.get("deadline", "")
        is_completed = self.request.GET.get("is_completed", False)
        priority = self.request.GET.get("priority", "")
        task_type = self.request.GET.get("task_type", "")
        project = self.request.GET.get("project", "")
        no_assignees = self.request.GET.get("no_assignees", False)
        context["search_form"] = TaskSearchForm(
            initial={
                "name": name,
                "is_completed": is_completed,
                "deadline": deadline,
                "priority": priority,
                "task_type": task_type,
                "project": project,
                "no_assignees": no_assignees,
            }
        )
        return context

    def get_queryset(self):
        queryset = Task.objects.select_related("project")
        form = TaskSearchForm(self.request.GET)

        if form.is_valid():
            deadline = form.cleaned_data.get("deadline")
            priority = form.cleaned_data["priority"]
            task_type = form.cleaned_data["task_type"]
            project = form.cleaned_data["project"]
            name = form.cleaned_data["name"]
            is_completed = form.cleaned_data["is_completed"]
            no_assignees = form.cleaned_data["no_assignees"]

            if name:
                queryset = queryset.filter(name__icontains=name)
            if is_completed:
                queryset = queryset.filter(is_completed=is_completed)
            if deadline:
                queryset = queryset.filter(deadline__lte=deadline)
            if priority:
                queryset = queryset.filter(priority=priority)
            if task_type:
                queryset = queryset.filter(task_type__name=task_type)
            if project:
                queryset = queryset.filter(project__name=project)
            if no_assignees:
                queryset = queryset.filter(assignees=None)

        return queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task

    def post(self, request, *args, **kwargs):
        update_task = self.get_object()
        new_assignee = request.user
        if new_assignee in update_task.assignees.all():
            update_task.assignees.remove(new_assignee)
        else:
            update_task.assignees.add(new_assignee)
        return redirect("manager:task-detail", pk=update_task.pk)


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm

    def get_success_url(self):
        return reverse_lazy("manager:task-detail", kwargs={"pk": self.object.pk})


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm

    def get_success_url(self):
        return reverse_lazy("manager:task-detail", kwargs={"pk": self.object.pk})


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("manager:task-list")


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)
        last_name = self.request.GET.get("last_name", "")
        position = self.request.GET.get("position", "")
        team = self.request.GET.get("team", "")
        context["search_form"] = WorkerSearchForm(
            initial={
                "last_name": last_name,
                "position": position,
                "team": team,
            }
        )
        return context

    def get_queryset(self):
        queryset = Worker.objects.select_related("position")

        form = WorkerSearchForm(self.request.GET)

        if form.is_valid():
            last_name = form.cleaned_data["last_name"]
            position = form.cleaned_data["position"]
            team = form.cleaned_data["team"]

            if last_name:
                queryset = queryset.filter(last_name__icontains=last_name)
            if position:
                queryset = queryset.filter(position__name=position)
            if team:
                queryset = queryset.filter(team__name=team)

        return queryset

class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["worker_is_manager"] = self.object.groups.filter(name="Manager").exists()
        return context

    def post(self, request, *args, **kwargs):
        if request.user.has_perm("workers.add_worker"):
            update_worker = self.get_object()
            manager_group = get_object_or_404(Group, name="Manager")
            if manager_group in update_worker.groups.all():
                update_worker.groups.remove(manager_group)
            else:
                update_worker.groups.add(manager_group)
            return redirect("manager:worker-detail", pk=update_worker.pk)


class WorkerCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm
    permission_required = "workers.add_worker"


class WorkerUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerUpdateForm

    def get_object(self, queryset=None):
        if not hasattr(self, "_object"):
            self._object = super().get_object(queryset)
        return self._object

    def test_func(self):
        update_user = self.get_object()
        return (
            self.request.user == update_user
            or self.request.user.has_perm("workers.add_worker")
        )

    def handle_no_permission(self):
        raise PermissionDenied

    def get_success_url(self):
        return reverse_lazy("manager:worker-detail", kwargs={"pk": self.object.pk})


class WorkerPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    model = Worker


class WorkerDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = Worker
    permission_required = "workers.delete_worker"
    success_url = reverse_lazy("manager:worker-list")


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

    def get_context_data(self, **kwargs):
        context = super(PositionListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = PositionSearchForm(
            initial={
                "name": name,
            }
        )
        return context

    def get_queryset(self):
        queryset = Position.objects.all()
        form = PositionSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data["name"]
            if name:
                queryset = queryset.filter(name__icontains=name)
        return queryset


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

    def get_context_data(self, **kwargs):
        context = super(TaskTypeListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TaskTypeSearchForm(
            initial={
                "name": name,
            }
        )
        return context

    def get_queryset(self):
        queryset = Position.objects.all()
        form = TaskTypeSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data["name"]
            if name:
                queryset = queryset.filter(name__icontains=name)
        return queryset


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

    def get_context_data(self, **kwargs):
        context = super(TeamListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        projects = self.request.GET.get("projects", "")
        no_team_members = self.request.GET.get("no_team_members", False)
        context["search_form"] = TeamSearchForm(
            initial={
                "name": name,
                "projects": projects,
                "no_team_members": no_team_members,
            }
        )
        return context

    def get_queryset(self):
        queryset = Team.objects.all()
        form = TeamSearchForm(self.request.GET)

        if form.is_valid():
            name = form.cleaned_data["name"]
            projects = form.cleaned_data["projects"]
            no_team_members = form.cleaned_data["no_team_members"]

            if name:
                queryset = queryset.filter(name__icontains=name)
            if projects:
                for project in projects:
                    queryset = queryset.filter(projects__name=project.name)
            if no_team_members:
                queryset = queryset.filter(worker=None)

        return queryset


class TeamDetailView(LoginRequiredMixin, generic.DetailView):
    model = Team


class TeamCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Team
    fields = "__all__"
    permission_required = "teams.add_team"

    def get_success_url(self):
        return reverse_lazy("manager:team-detail", kwargs={"pk": self.object.pk})


class TeamUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = Team
    fields = "__all__"
    # form_class = TeamUpdateForm
    permission_required = "teams.change_team"

    def get_success_url(self):
        return reverse_lazy("manager:team-detail", kwargs={"pk": self.object.pk})


class TeamDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = Team
    permission_required = "teams.delete_team"
    success_url = reverse_lazy("manager:team-list")

