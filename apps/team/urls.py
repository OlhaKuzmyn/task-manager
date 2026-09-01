from django.urls import path

from apps.team.views import (
    TeamListView,
    TeamDetailView,
    TeamCreateView,
    TeamUpdateView,
    TeamDeleteView
)

app_name = "team"

urlpatterns = [
    path("", TeamListView.as_view(), name="team-list"),
    path("<int:pk>/", TeamDetailView.as_view(), name="team-detail"),
    path("create/", TeamCreateView.as_view(), name="team-create"),
    path("update/<int:pk>/", TeamUpdateView.as_view(), name="team-update"),
    path("delete/<int:pk>/", TeamDeleteView.as_view(), name="team-delete"),
]