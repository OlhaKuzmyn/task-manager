from django.urls import path

from manager.models import Position
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
    PositionListView,
    PositionCreateView,
    ProjectDeleteView,
    PositionUpdateView,
    PositionDeleteView,
    TaskTypeListView,
    TaskTypeCreateView,
    TaskTypeUpdateView,
    TaskTypeDeleteView,
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
    path("projects/delete/<int:pk>/", ProjectDeleteView.as_view(), name="project-delete"),
    path("positions/", PositionListView.as_view(), name="position-list"),
    path("positions/create", PositionCreateView.as_view(), name="position-create"),
    path("positions/update/<int:pk>/", PositionUpdateView.as_view(), name="position-update"),
    path("positions/delete/<int:pk>/", PositionDeleteView.as_view(), name="position-delete"),
    path("task-type/", TaskTypeListView.as_view(), name="task-type-list"),
    path("task-type/create", TaskTypeCreateView.as_view(), name="task-type-create"),
    path("task-type/update/<int:pk>/", TaskTypeUpdateView.as_view(), name="task-type-update"),
    path("task-type/delete/<int:pk>/", TaskTypeDeleteView.as_view(), name="task-type-delete"),
]
