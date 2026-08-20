from django.urls import path

from manager.views import (
    index,
    TaskListView,
    TaskDetailView,
    WorkerListView,
    WorkerDetailView,
    ProjectListView,
    ProjectCreateView,
    ProjectDetailView,
    ProjectUpdateView,
)

app_name = "manager"

urlpatterns = [
    path("", index, name="index"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
    path("projects/", ProjectListView.as_view(), name="project-list"),
    path("projects/<int:pk>/", ProjectDetailView.as_view(), name="project-detail"),
    path("projects/create", ProjectCreateView.as_view(), name="project-create"),
    path("projects/update/<int:pk>/", ProjectUpdateView.as_view(), name="project-update"),
]
