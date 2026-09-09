from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.urls import reverse_lazy
from django.views import generic

from apps.project.forms import ProjectSearchForm
from apps.project.models import Project


class ProjectListView(LoginRequiredMixin, generic.ListView):
    model = Project
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        no_tasks = self.request.GET.get("no_tasks", False)
        context["search_form"] = ProjectSearchForm(
            initial={
                "name": name,
                "no_tasks": no_tasks,
            }
        )
        return context

    def get_queryset(self):
        queryset = Project.objects.all()
        form = ProjectSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data["name"]
            if name:
                queryset = queryset.filter(name__icontains=name)
            if form.cleaned_data["no_tasks"]:
                queryset = queryset.filter(task__isnull=True)
        return queryset


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    model = Project


class ProjectCreateView(
    LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView
):
    model = Project
    fields = "__all__"
    permission_required = "project.add_project"

    def get_success_url(self):
        return reverse_lazy(
            "project:project-detail",
            kwargs={"pk": self.object.pk}
        )


class ProjectUpdateView(
    LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView
):
    model = Project
    fields = "__all__"
    permission_required = "project.change_project"

    def get_success_url(self):
        return reverse_lazy(
            "project:project-detail",
            kwargs={"pk": self.object.pk}
        )


class ProjectDeleteView(
    LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView
):
    model = Project
    permission_required = "project.delete_project"
    success_url = reverse_lazy("project:project-list")
