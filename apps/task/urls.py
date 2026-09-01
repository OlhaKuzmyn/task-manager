from django.urls import path

from apps.task.views import (
    TaskListView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    TaskDetailView
)

app_name = "task"

urlpatterns = [
    path("", TaskListView.as_view(), name="task-list"),
    path("create", TaskCreateView.as_view(), name="task-create"),
    path("update/<int:pk>/", TaskUpdateView.as_view(), name="task-update"),
    path("delete/<int:pk>/", TaskDeleteView.as_view(), name="task-delete"),
    path("<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
]
