from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.urls import reverse_lazy
from django.views import generic

from apps.task_type.forms import TaskTypeSearchForm
from apps.task_type.models import TaskType


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    paginate_by = 5
    template_name = "task_type/task_type_list.html"
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
        queryset = TaskType.objects.all()
        form = TaskTypeSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data["name"]
            if name:
                queryset = queryset.filter(name__icontains=name)
        return queryset


class TaskTypeCreateView(
    LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView
):
    model = TaskType
    fields = "__all__"
    permission_required = "task_type.add_tasktype"
    template_name = "task_type/task_type_form.html"
    success_url = reverse_lazy("task_type:task-type-list")


class TaskTypeUpdateView(
    LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView
):
    model = TaskType
    fields = "__all__"
    permission_required = "task_type.change_tasktype"
    template_name = "task_type/task_type_form.html"
    success_url = reverse_lazy("task_type:task-type-list")


class TaskTypeDeleteView(
    LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView
):
    model = TaskType
    permission_required = "task_type.delete_tasktype"
    template_name = "task_type/task_type_confirm_delete.html"
    success_url = reverse_lazy("task_type:task-type-list")
