from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.contrib.auth.models import Group
from django.contrib.auth.views import PasswordChangeView
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from apps.worker.forms import (
    WorkerUpdateForm,
    WorkerCreationForm,
    WorkerSearchForm
)
from apps.worker.models import Worker


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

    def post(self, request, *args, **kwargs):
        if request.user.has_perm("worker.add_worker"):
            update_worker = self.get_object()
            manager_group = get_object_or_404(Group, name="Manager")
            if manager_group in update_worker.groups.all():
                update_worker.groups.remove(manager_group)
                update_worker.is_manager = False
                update_worker.save()
            else:
                update_worker.is_manager = True
                update_worker.save()
                update_worker.groups.add(manager_group)
            return redirect("worker:worker-detail", pk=update_worker.pk)


class WorkerCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.CreateView
):
    model = Worker
    form_class = WorkerCreationForm
    permission_required = "worker.add_worker"


class WorkerUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.UpdateView
):
    model = Worker
    form_class = WorkerUpdateForm

    def get_object(self, queryset=None):
        if not hasattr(self, "_object"):
            self._object = super().get_object(queryset)
        return self._object

    def test_func(self):
        update_user = self.get_object()
        return self.request.user == update_user or self.request.user.has_perm(
            "worker.change_worker"
        )

    def handle_no_permission(self):
        raise PermissionDenied

    def get_success_url(self):
        return reverse_lazy(
            "worker:worker-detail",
            kwargs={"pk": self.object.pk}
        )


class WorkerPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    model = Worker


class WorkerDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.DeleteView
):
    model = Worker
    permission_required = "worker.delete_worker"
    success_url = reverse_lazy("worker:worker-list")
