from django.urls import path

from apps.project.views import (
    ProjectListView,
    ProjectDetailView,
    ProjectCreateView,
    ProjectDeleteView,
    ProjectUpdateView,
)

app_name = "project"

urlpatterns = [
    path("", ProjectListView.as_view(), name="project-list"),
    path("<int:pk>/", ProjectDetailView.as_view(), name="project-detail"),
    path("create/", ProjectCreateView.as_view(), name="project-create"),
    path(
        "update/<int:pk>/",
        ProjectUpdateView.as_view(),
        name="project-update"
    ),
    path(
        "delete/<int:pk>/",
        ProjectDeleteView.as_view(),
        name="project-delete"
    ),
]
