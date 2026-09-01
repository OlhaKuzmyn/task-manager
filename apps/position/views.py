from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from apps.position.forms import PositionSearchForm
from apps.position.models import Position


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
    permission_required = "position.add_position"
    success_url = reverse_lazy("position:position-list")


class PositionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = Position
    fields = "__all__"
    permission_required = "position.change_position"
    success_url = reverse_lazy("position:position-list")

class PositionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = Position
    permission_required = "position.delete_position"
    success_url = reverse_lazy("position:position-list")
