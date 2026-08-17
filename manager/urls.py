from django.urls import path

from manager.views import index, TaskListView

app_name = "manager"

urlpatterns = [
    path("", index, name="index"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
]
