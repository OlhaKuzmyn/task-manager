from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.urls import reverse_lazy
from django.views import generic

from apps.team.forms import TeamForm, TeamSearchForm
from apps.team.models import Team


class TeamListView(LoginRequiredMixin, generic.ListView):
    model = Team
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(TeamListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        projects = self.request.GET.get("projects", "")
        no_team_members = self.request.GET.get("no_team_members", False)
        no_projects = self.request.GET.get("no_projects", False)
        context["search_form"] = TeamSearchForm(
            initial={
                "name": name,
                "projects": projects,
                "no_team_members": no_team_members,
                "no_projects": no_projects,
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
            no_projects = form.cleaned_data["no_projects"]

            if name:
                queryset = queryset.filter(name__icontains=name)
            if projects:
                for project in projects:
                    queryset = queryset.filter(projects__name=project.name)
            if no_team_members:
                queryset = queryset.filter(worker=None)
            if no_projects:
                queryset = queryset.filter(projects__isnull=True)

        return queryset


class TeamDetailView(LoginRequiredMixin, generic.DetailView):
    model = Team


class TeamCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.CreateView
):
    model = Team
    form_class = TeamForm
    permission_required = "team.add_team"

    def get_success_url(self):
        return reverse_lazy("team:team-detail", kwargs={"pk": self.object.pk})


class TeamUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.UpdateView
):
    model = Team
    form_class = TeamForm
    permission_required = "team.change_team"

    def get_success_url(self):
        return reverse_lazy("team:team-detail", kwargs={"pk": self.object.pk})


class TeamDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.DeleteView
):
    model = Team
    permission_required = "team.delete_team"
    success_url = reverse_lazy("team:team-list")
