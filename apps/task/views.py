from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from apps.task.models import Task
from apps.task.forms import TaskForm, TaskSearchForm
from apps.team.models import Team


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        context["search_form"] = TaskSearchForm(
            self.request.GET or {"filter_select": "mine_and_team"}
        )
        return context

    def get_queryset(self):
        if self.request.user.team:
            user_team_projects = Team.objects.get(worker__id=self.request.user.id).projects.all()
        form = TaskSearchForm(self.request.GET)

        filter_select = "mine_and_team"
        is_completed = no_assignees = False
        name = deadline = priority = task_type = project = None

        if form.is_valid():
            filter_select = form.cleaned_data["filter_select"] or "mine_and_team"
            deadline = form.cleaned_data["deadline"]
            priority = form.cleaned_data["priority"]
            task_type = form.cleaned_data["task_type"]
            project = form.cleaned_data["project"]
            name = form.cleaned_data["name"]
            is_completed = form.cleaned_data["is_completed"]
            no_assignees = form.cleaned_data["no_assignees"]


        if filter_select == "all":
            queryset = Task.objects.all()
        elif filter_select == "mine_and_team" and self.request.user.team:
            queryset = Task.objects.filter(Q(project__in=user_team_projects) | Q(assignees=self.request.user))
        elif filter_select == "team" and self.request.user.team:
            queryset = Task.objects.filter(Q(project__in=user_team_projects))
        else:
            queryset = Task.objects.filter(assignees=self.request.user)

        queryset = queryset.select_related("project").distinct()

        if is_completed:
            queryset = queryset.filter(is_completed=True)
        else:
            queryset = queryset.filter(is_completed=False)

        if name:
            queryset = queryset.filter(name__icontains=name)
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
        return redirect("task:task-detail", pk=update_task.pk)


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm

    def get_success_url(self):
        return reverse_lazy("task:task-detail", kwargs={"pk": self.object.pk})


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm

    def get_success_url(self):
        return reverse_lazy("task:task-detail", kwargs={"pk": self.object.pk})


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task:task-list")
