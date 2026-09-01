from django.urls import path

from apps.task_type.views import TaskTypeListView, TaskTypeCreateView, TaskTypeUpdateView, TaskTypeDeleteView

app_name = "task_type"

urlpatterns = [
    path("", TaskTypeListView.as_view(), name="task-type-list"),
    path("create/", TaskTypeCreateView.as_view(), name="task-type-create"),
    path("update/<int:pk>/", TaskTypeUpdateView.as_view(), name="task-type-update"),
    path("delete/<int:pk>/", TaskTypeDeleteView.as_view(), name="task-type-delete"),
]
